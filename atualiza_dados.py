# atualiza_dados.py
import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)

# ----------------------- carregar credenciais -----------------------


def _coerce_empresas(val):
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return json.loads(val)
    return []


EMPRESAS = []

# 1) via st.secrets (quando rodar dentro do Streamlit Cloud)
try:
    import streamlit as st  # type: ignore

    if "EMPRESAS" in st.secrets:
        EMPRESAS = _coerce_empresas(st.secrets["EMPRESAS"])
except Exception:
    pass

# 2) via .streamlit/secrets.toml (local)
if not EMPRESAS:
    toml_path = BASE_DIR / ".streamlit" / "secrets.toml"
    if toml_path.exists():
        try:
            import tomllib  # py3.11+
            data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
            EMPRESAS = _coerce_empresas(
                data.get("EMPRESAS") or data.get("EMPRESAS_JSON")
            )
        except Exception:
            pass

# 3) fallback: empresas_config.json
if not EMPRESAS:
    json_path = BASE_DIR / "empresas_config.json"
    if json_path.exists():
        EMPRESAS = _coerce_empresas(json_path.read_text(encoding="utf-8"))

if not EMPRESAS:
    raise RuntimeError(
        "Nenhuma credencial encontrada em: "
        "st.secrets['EMPRESAS'], .streamlit/secrets.toml ou empresas_config.json"
    )

# ----------------------- helpers -----------------------


def obter_token(login: str, senha: str) -> str:
    """Obtém token de autenticação na API Sonax."""
    r = requests.post(
        "https://apiv2.sonax.net.br/login",
        json={"id": login, "senha": senha},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["data"]["token"]


def _parse_data(df: pd.DataFrame) -> pd.DataFrame:
    """Garante a coluna dt_inicio a partir de alguma coluna de data existente."""
    for c in ["dt_inicio", "data", "dt", "data_inicio", "datahora", "created_at"]:
        if c in df.columns:
            df["dt_inicio"] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")
            break
    if "dt_inicio" not in df.columns:
        df["dt_inicio"] = pd.NaT
    return df


def _mask_agente_por_alias(df: pd.DataFrame, alias: int) -> pd.Series:
    """
    Retorna máscara booleana selecionando SOMENTE registros desse alias (ramal).

    Não usa nome do agente de forma nenhuma, exatamente para evitar “vazar” ligações
    de outro agente que por acaso tenha mesmo nome.
    """
    if df.empty:
        return pd.Series(False, index=df.index)

    alias_cols = [
        "alias",
        "id_alias",
        "idagente",
        "id_agente",
        "ramal",
        "id_ramal",
        "id_usuario",
        "idusuario",
        "id_operador",
        "idoperador",
    ]

    m_alias = pd.Series(False, index=df.index)
    for col in alias_cols:
        if col in df.columns:
            try:
                m_alias |= df[col].astype(str) == str(alias)
            except Exception:
                # se der problema de tipo em alguma coluna, ignora aquela coluna
                pass

    return m_alias


def buscar_ultimos_dias(alias: int, dias: int = 7, debug: bool = True) -> pd.DataFrame:
    """
    Busca nas APIs de TODAS as empresas configuradas,
    junta tudo e filtra SOMENTE as ligações que passaram pelo alias informado.
    """
    fim = date.today()
    inicio = fim - timedelta(days=dias)
    todos: list[dict] = []

    for emp in EMPRESAS:
        empresa = emp.get("empresa", "<sem_nome>")
        try:
            token = obter_token(emp["login"], emp["senha"])
        except Exception as e:
            if debug:
                print(f"[ERRO TOKEN] {empresa}: {e}")
            continue

        body = {
            "dt_inicio": inicio.strftime("%d/%m/%Y"),
            "dt_fim": fim.strftime("%d/%m/%Y"),
        }

        try:
            resp = requests.post(
                "https://apiv2.sonax.net.br/api/vingadora/relatorioEntrante",
                data=body,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "token": token,
                },
                timeout=60,
            )
            j = resp.json()
            relatorio = j.get("relatorio", [])
        except Exception as e:
            if debug:
                print(f"[ERRO DADOS] {empresa}: {e}")
            continue

        if debug:
            print(f"[INFO] {empresa}: {len(relatorio)} linhas")

        # marca empresa em cada registro
        for r in relatorio:
            r["Empresa"] = empresa

        todos.extend(relatorio)

    df = pd.DataFrame(todos)
    if df.empty:
        if debug:
            print("[INFO] Nenhum registro retornado de nenhuma empresa.")
        return df

    # Normalização de data
    df = _parse_data(df)

    # Deduplicação por ligação (quando houver identificador único)
    dedup_key = None
    for cand in ["uniqueid", "unique_id", "id_chamada", "uuid", "call_id"]:
        if cand in df.columns:
            dedup_key = cand
            break

    if dedup_key:
        df = df.drop_duplicates(subset=[dedup_key], keep="last")
    else:
        df = df.drop_duplicates(keep="last")

    # Garante coluna de contagem
    if "total_ligacoes" not in df.columns:
        df["total_ligacoes"] = 1

    # Filtro por alias (ramal)
    masc = _mask_agente_por_alias(df, alias=alias)
    if debug:
        print(f"[INFO] Filtro por alias={alias} -> {masc.sum()} linhas")
    df = df[masc].copy()

    return df


def atualizar_cache(alias: int, dias: int = 7, debug: bool = True):
    """
    Atualiza o parquet do alias informado.

    - Busca últimos `dias` em TODAS as empresas.
    - Filtra pelo alias.
    - Junta com o que já existe no parquet (se houver) e remove duplicados.
    """
    arq = DADOS_DIR / f"dados_{alias}.parquet"
    novos = buscar_ultimos_dias(alias, dias=dias, debug=debug)

    if arq.exists():
        try:
            antigos = pd.read_parquet(arq)
        except Exception:
            antigos = pd.DataFrame()
        df = pd.concat([antigos, novos], ignore_index=True).drop_duplicates()
    else:
        df = novos

    if not df.empty:
        df.to_parquet(arq, index=False)
        if debug:
            print(f"[OK] Alias {alias}: {len(df)} registros salvos em {arq.name}")
    else:
        if debug:
            print(f"[WARN] Alias {alias}: nada para salvar.")


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description=(
            "Atualiza o cache .parquet de um alias (ramal) específico, "
            "buscando em todas as empresas configuradas."
        )
    )
    p.add_argument("--alias", type=int, required=True, help="Ramal / alias do agente")
    p.add_argument(
        "--dias",
        type=int,
        default=30,
        help="Quantidade de dias para trás a partir de hoje (default: 30)",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="Mostra logs de depuração no console",
    )
    args = p.parse_args()

    atualizar_cache(args.alias, dias=args.dias, debug=args.debug)
