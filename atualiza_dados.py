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
# 1) st.secrets
try:
    import streamlit as st  # type: ignore
    if "EMPRESAS" in st.secrets:
        EMPRESAS = _coerce_empresas(st.secrets["EMPRESAS"])
except Exception:
    pass

# 2) .streamlit/secrets.toml
if not EMPRESAS:
    toml_path = BASE_DIR / ".streamlit" / "secrets.toml"
    if toml_path.exists():
        try:
            import tomllib  # py3.11+
            data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
            EMPRESAS = _coerce_empresas(data.get("EMPRESAS") or data.get("EMPRESAS_JSON"))
        except Exception:
            pass

# 3) fallback
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
    r = requests.post(
        "https://apiv2.sonax.net.br/login",
        json={"id": login, "senha": senha},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["data"]["token"]


def _parse_data(df: pd.DataFrame) -> pd.DataFrame:
    # escolhe a primeira coluna de data existente e cria dt_inicio
    for c in ["dt_inicio", "data", "dt", "data_inicio", "datahora", "created_at"]:
        if c in df.columns:
            df["dt_inicio"] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")
            break
    if "dt_inicio" not in df.columns:
        df["dt_inicio"] = pd.NaT
    return df


def _mask_agente(df: pd.DataFrame, alias: int, nome_agente: str | None = None) -> pd.Series:
    """Retorna máscara booleana: (alias bate) OU (nome_agente bate) quando disponíveis."""
    if df.empty:
        return pd.Series(False, index=df.index)

    # alias/ramal candidatos
    alias_cols = ["alias", "id_alias", "idagente", "id_agente", "ramal", "id_ramal", "id_usuario"]
    m_alias = pd.Series(False, index=df.index)
    for col in alias_cols:
        if col in df.columns:
            try:
                m_alias |= (df[col].astype(str) == str(alias))
            except Exception:
                pass

    # reforço por nome (opcional)
    m_nome = pd.Series(False, index=df.index)
    if nome_agente:
        nome_norm = str(nome_agente).strip().upper()
        name_cols = ["agente", "agent_name", "nm_agente", "operador", "usuario", "user_name", "nome"]
        for col in name_cols:
            if col in df.columns:
                try:
                    m_nome |= (df[col].astype(str).str.upper().str.strip() == nome_norm)
                except Exception:
                    pass

    # se temos nome, usa (alias OR nome); senão, só alias
    return (m_alias | m_nome) if nome_agente else m_alias


def buscar_ultimos_dias(alias: int, dias: int = 7, nome_agente: str | None = None, debug: bool = True) -> pd.DataFrame:
    fim = date.today()
    inicio = fim - timedelta(days=dias)
    todos = []

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
                headers={"Content-Type": "application/x-www-form-urlencoded", "token": token},
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
        for r in relatorio:
            r["Empresa"] = empresa
        todos.extend(relatorio)

    df = pd.DataFrame(todos)
    if df.empty:
        if debug:
            print("[INFO] Nenhum registro retornado.")
        return df

    # normalizações
    df = _parse_data(df)

    # dedup por chamada quando possível (evita múltiplos eventos da mesma ligação)
    dedup_key = None
    for cand in ["uniqueid", "unique_id", "id_chamada", "uuid", "call_id"]:
        if cand in df.columns:
            dedup_key = cand
            break
    if dedup_key:
        df = df.drop_duplicates(subset=["Empresa", dedup_key], keep="last")
    else:
        df = df.drop_duplicates(keep="last")

    # contagem
    if "total_ligacoes" not in df.columns:
        df["total_ligacoes"] = 1

    # filtro por agente
    masc = _mask_agente(df, alias=alias, nome_agente=nome_agente)
    if debug:
        print(f"[INFO] Filtro agente (alias={alias}, nome={nome_agente or '-'}) -> {masc.sum()} linhas")
    df = df[masc].copy()

    return df


def atualizar_cache(alias: int, dias: int = 7, nome_agente: str | None = None, debug: bool = True):
    arq = DADOS_DIR / f"dados_{alias}.parquet"
    novos = buscar_ultimos_dias(alias, dias=dias, nome_agente=nome_agente, debug=debug)

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

    p = argparse.ArgumentParser()
    p.add_argument("--alias", type=int, required=True)
    p.add_argument(
        "--nome",
        type=str,
        default=None,
        help="Opcional: reforço por nome do agente (ex.: 'AMANDA MARIANO')",
    )
    p.add_argument("--dias", type=int, default=30)
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()

    atualizar_cache(args.alias, dias=args.dias, nome_agente=args.nome, debug=args.debug)
