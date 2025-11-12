import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import json
import os

# Diretório base
BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)

# Carregar empresas
import streamlit as st
EMPRESAS = st.secrets["EMPRESAS"]


# --- Usuários (agentes) e alias ---
USERS = {
    "ALESSANDRA SOUZA": {"alias": 309},
    "AMANDA MARIANO": {"alias": 504},
    "AMANDA RIBEIRO": {"alias": 511},
    "ANGELICA": {"alias": 365},
    "ATALIANE": {"alias": 323},
    "CAMILA SILVA": {"alias": 321},
    "CARLA": {"alias": 366},
    "CARLINE": {"alias": 362},
    "CAROLINA LUIZA": {"alias": 502},
    "CAROLINA PAULINO": {"alias": 311},
    "CATHARINE": {"alias": 315},
    "CHAENE": {"alias": 324},
    "DANIELA MARTINS": {"alias": 513},
    "DEBORA CARLA": {"alias": 521},
    "DEBORA VENANCIO": {"alias": 508},
    "DERICK": {"alias": 524},
    "DIANDRA": {"alias": 525},
    "GLEICE": {"alias": 503},
    "IVANIA": {"alias": 507},
    "JANIELE": {"alias": 318},
    "JESSICA": {"alias": 516},
    "KATYLEN": {"alias": 320},
    "LAYSSA": {"alias": 307},
    "LEILA": {"alias": 322},
    "LETICIA GUIDO": {"alias": 319},
    "LIVIA": {"alias": 514},
    "LUAN": {"alias": 364},
    "LUCAS": {"alias": 327},
    "MARA": {"alias": 310},
    "MARCELA MOREIRA": {"alias": 363},
    "MARCILENE": {"alias": 325},
    "MARCO SENEDO": {"alias": 317},
    "MARIA ALICE": {"alias": 314},
    "MARIANGELA": {"alias": 520},
    "MAYARA ALVES": {"alias": 361},
    "MICHELE BITARES": {"alias": 312},
    "MYCHELE": {"alias": 518},
    "NAIARA": {"alias": 328},
    "OTAVIO": {"alias": 515},
    "PAULA": {"alias": 316},
    "ROSARIO": {"alias": 300},
    "SAMARA": {"alias": 304},
    "SEBASTIÃO NETO": {"alias": 523},
    "SIMONE": {"alias": 360},
    "TATIANA FERREIRA": {"alias": 505},
    "TATIANE ROCHA": {"alias": 509},
    "THAMARA": {"alias": 303},
    "THAYS R.": {"alias": 308},
    "VIVIANE": {"alias": 305},
    "BARBARA": {"alias": 302},
    "PAULO": {"alias": 367},
    "GEISSY": {"alias": 369},
    "JOSIANE": {"alias": 368},
    "LUCAS 2": {"alias": 372},
    "ELIENE": {"alias": 371},
    "ENRICK": {"alias": 370},
    "CRISTIANA FERREIRA": {"alias": 500},
    "ROBERTO SOARES": {"alias": 103},
    "SABRINA VIEIRA": {"alias": 301},
    "ALLYNE ALVES": {"alias": 306},
    "RAISSA GOMES": {"alias": 325},
    "ELAINE CUNHA": {"alias": 313},
    "LAYSLA ALVES": {"alias": 519},
    "CAMILA BALBINO": {"alias": 306},
}

def obter_token(login: str, senha: str) -> str:
    url_login = "https://apiv2.sonax.net.br/login"
    payload = {"id": login, "senha": senha}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url_login, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["data"]["token"]

def buscar_ultimos_dias(alias: int, dias: int = 1) -> pd.DataFrame:
    fim = date.today()
    inicio = fim - timedelta(days=dias)
    todos = []

    for emp in EMPRESAS:
        try:
            token = obter_token(emp["login"], emp["senha"])
        except Exception as e:
            print(f"Erro token {emp['empresa']}: {e}")
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
            relatorio = resp.json().get("relatorio", [])
            for r in relatorio:
                r["Empresa"] = emp["empresa"]
            todos.extend(relatorio)
        except Exception as e:
            print(f"Erro dados {emp['empresa']}: {e}")

    df = pd.DataFrame(todos)
    if "alias" in df.columns:
        df = df[df["alias"].astype(str) == str(alias)]

    if df.empty:
        return df

    df["dt_inicio"] = pd.to_datetime(df["dt_inicio"], dayfirst=True, errors="coerce")
    df["total_ligacoes"] = 1
    return df

def atualizar_cache(alias: int):
    arquivo = DADOS_DIR / f"dados_{alias}.parquet"
    novos = buscar_ultimos_dias(alias)

    if arquivo.exists():
        antigos = pd.read_parquet(arquivo)
        df = pd.concat([antigos, novos], ignore_index=True).drop_duplicates()
    else:
        df = novos

    if not df.empty:
        df.to_parquet(arquivo, index=False)
        print(f"✅ Alias {alias}: {len(df)} registros atualizados.")
    else:
        print(f"⚠️ Alias {alias}: Nenhum dado novo.")

if __name__ == "__main__":
    for user, info in USERS.items():
        atualizar_cache(info["alias"])
