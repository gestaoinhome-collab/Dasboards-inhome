import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import subprocess

# =====================================================================
# 0) DIRETÓRIOS / ARQUIVOS
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)

# =====================================================================
# 1) CONFIGURAÇÃO DE USUÁRIOS (LOGIN -> ALIAS)
#    Depois você troca pelos agentes reais
# =====================================================================
USERS = {
    "ALESSANDRA SOUZA": {"senha": "1234", "alias": 309},
    "AMANDA MARIANO": {"senha": "1234", "alias": 504},
    "AMANDA RIBEIRO": {"senha": "1234", "alias": 511},
    "ANGELICA": {"senha": "1234", "alias": 365},
    "ATALIANE": {"senha": "1234", "alias": 323},
    "CAMILA SILVA": {"senha": "1234", "alias": 321},
    "CARLA": {"senha": "1234", "alias": 366},
    "CARLINE": {"senha": "1234", "alias": 362},
    "CAROLINA LUIZA": {"senha": "1234", "alias": 502},
    "CAROLINA PAULINO": {"senha": "1234", "alias": 311},
    "CATHARINE": {"senha": "1234", "alias": 315},
    "CHAENE": {"senha": "1234", "alias": 324},
    "DANIELA MARTINS": {"senha": "1234", "alias": 513},
    "DEBORA CARLA": {"senha": "1234", "alias": 521},
    "DEBORA VENANCIO": {"senha": "1234", "alias": 508},
    "DERICK": {"senha": "1234", "alias": 524},
    "DIANDRA": {"senha": "1234", "alias": 525},
    "GLEICE": {"senha": "1234", "alias": 503},
    "IVANIA": {"senha": "1234", "alias": 507},
    "JANIELE": {"senha": "1234", "alias": 318},
    "JESSICA": {"senha": "1234", "alias": 516},
    "KATYLEN": {"senha": "1234", "alias": 320},
    "LAYSSA": {"senha": "1234", "alias": 307},
    "LEILA": {"senha": "1234", "alias": 322},
    "LETICIA GUIDO": {"senha": "1234", "alias": 319},
    "LIVIA": {"senha": "1234", "alias": 514},
    "LUAN": {"senha": "1234", "alias": 364},
    "LUCAS": {"senha": "1234", "alias": 327},
    "MARA": {"senha": "1234", "alias": 310},
    "MARCELA MOREIRA": {"senha": "1234", "alias": 363},
    "MARCILENE": {"senha": "1234", "alias": 325},
    "MARCO SENEDO": {"senha": "1234", "alias": 317},
    "MARIA ALICE": {"senha": "1234", "alias": 314},
    "MARIANGELA": {"senha": "1234", "alias": 520},
    "MAYARA ALVES": {"senha": "1234", "alias": 361},
    "MICHELE BITARES": {"senha": "1234", "alias": 312},
    "MYCHELE": {"senha": "1234", "alias": 518},
    "NAIARA": {"senha": "1234", "alias": 328},
    "OTAVIO": {"senha": "1234", "alias": 515},
    "PAULA": {"senha": "1234", "alias": 316},
    "ROSARIO": {"senha": "1234", "alias": 300},
    "SAMARA": {"senha": "1234", "alias": 304},
    "SEBASTIÃO NETO": {"senha": "1234", "alias": 523},
    "SIMONE": {"senha": "1234", "alias": 360},
    "TATIANA FERREIRA": {"senha": "1234", "alias": 505},
    "TATIANE ROCHA": {"senha": "1234", "alias": 509},
    "THAMARA": {"senha": "1234", "alias": 303},
    "THAYS R.": {"senha": "1234", "alias": 308},
    "VIVIANE": {"senha": "1234", "alias": 305},
    "BARBARA": {"senha": "1234", "alias": 302},
    "PAULO": {"senha": "1234", "alias": 367},
    "GEISSY": {"senha": "1234", "alias": 369},
    "JOSIANE": {"senha": "1234", "alias": 368},
    "LUCAS 2": {"senha": "1234", "alias": 372},
    "ELIENE": {"senha": "1234", "alias": 371},
    "ENRICK": {"senha": "1234", "alias": 370},
    "CRISTIANA FERREIRA": {"senha": "1234", "alias": 500},
    "ROBERTO SOARES": {"senha": "1234", "alias": 103},
    "SABRINA VIEIRA": {"senha": "1234", "alias": 301},
    "ALLYNE ALVES": {"senha": "1234", "alias": 306},
    "RAISSA GOMES": {"senha": "1234", "alias": 325},
    "ELAINE CUNHA": {"senha": "1234", "alias": 313},
    "LAYSLA ALVES": {"senha": "1234", "alias": 519},
    "CAMILA BALBINO": {"senha": "1234", "alias": 306},
}

# =====================================================================
# 2) FUNÇÕES DE CACHE LOCAL (.parquet)
# =====================================================================
def carregar_dados_local(alias: int) -> pd.DataFrame:
    """Carrega o arquivo .parquet do agente. Se não existir, avisa o usuário."""
    arquivo = DADOS_DIR / f"dados_{alias}.parquet"
    if not arquivo.exists():
        st.warning(
            "Nenhum dado local encontrado para esse agente.\n"
            "Clique em '🔄 Atualizar Agora' para buscar na API e criar o arquivo."
        )
        return pd.DataFrame()
    return pd.read_parquet(arquivo)


def atualizar_agora():
    """Chama o script atualiza_dados.py para atualizar todos os agentes."""
    with st.spinner("Buscando dados diretamente na API... isso pode demorar ⏳"):
        # roda o script usando o mesmo Python da máquina
        subprocess.run(["python", "atualiza_dados.py"], cwd=str(BASE_DIR))
    st.success("Atualização concluída! Os arquivos locais foram atualizados. ✅")


# =====================================================================
# 3) CONFIG DO STREAMLIT
# =====================================================================
st.set_page_config(page_title="Dashboard de Ligações", layout="wide")
st.title("Dashboard de Ligações - Agentes")

# =====================================================================
# 4) LOGIN
# =====================================================================
if "usuario" not in st.session_state:
    with st.form("login"):
        user = st.text_input("Usuário")
        pwd = st.text_input("Senha", type="password")
        entrou = st.form_submit_button("Entrar")

    if entrou:
        if user in USERS and USERS[user]["senha"] == pwd:
            st.session_state["usuario"] = user
            st.session_state["alias"] = USERS[user]["alias"]
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.stop()

# =====================================================================
# 5) DASHBOARD (DEPOIS DO LOGIN)
# =====================================================================
usuario = st.session_state["usuario"]
alias = st.session_state["alias"]

st.subheader(f"Agente: {usuario} (alias {alias})")

# Botão de atualização manual
if st.button("🔄 Atualizar Agora"):
    atualizar_agora()

# Carrega dados locais
df = carregar_dados_local(alias)

if df is None or df.empty:
    st.stop()

# =====================================================================
# 6) PREPARAÇÃO DOS DADOS (datas, ano, mês, dia)
# =====================================================================
if "dt_inicio" in df.columns:
    df["dt_inicio"] = pd.to_datetime(df["dt_inicio"], dayfirst=True, errors="coerce")
else:
    st.error("Coluna 'dt_inicio' não encontrada nos dados. Verifique o arquivo gerado.")
    st.stop()

df["dia"] = df["dt_inicio"].dt.day
df["mes"] = df["dt_inicio"].dt.month
df["ano"] = df["dt_inicio"].dt.year

# Garante a coluna de contagem
if "total_ligacoes" not in df.columns:
    df["total_ligacoes"] = 1

# =====================================================================
# 7) FILTROS (ANO / MÊS) EM CIMA DOS DADOS LOCAIS
# =====================================================================
anos_disponiveis = sorted(df["ano"].dropna().unique())
meses_nomes = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]
mes_map = {nome: i + 1 for i, nome in enumerate(meses_nomes)}

col_f1, col_f2 = st.columns(2)
with col_f1:
    ano_opcoes = ["Todos"] + [int(a) for a in anos_disponiveis]
    ano_sel = st.selectbox("Filtro Ano", ano_opcoes)
with col_f2:
    mes_sel = st.selectbox("Filtro Mês", ["Todos"] + meses_nomes)

# Aplica filtros
if ano_sel != "Todos":
    df = df[df["ano"] == int(ano_sel)]

if mes_sel != "Todos":
    mes_num = mes_map[mes_sel]
    df = df[df["mes"] == mes_num]

if df.empty:
    st.warning("Nenhum dado após aplicar os filtros selecionados.")
    st.stop()

# =====================================================================
# 8) MÉTRICAS DE TOPO
# =====================================================================
total_ligacoes = int(df["total_ligacoes"].sum())
total_empresas = df["Empresa"].nunique() if "Empresa" in df.columns else 0

m1, m2 = st.columns(2)
with m1:
    st.metric("Total Empresas", total_empresas)
with m2:
    st.metric("Total Ligações", f"{total_ligacoes:,}".replace(",", "."))

# =====================================================================
# 9) GRÁFICO DE LINHA - LIGAÇÕES POR DIA
# =====================================================================
if "dia" in df.columns:
    df_linha = df.groupby("dia", as_index=False)["total_ligacoes"].sum()
    fig_linha = px.line(df_linha, x="dia", y="total_ligacoes", title="Ligações por Dia")
    st.plotly_chart(fig_linha, use_container_width=True)

# =====================================================================
# 10) GRÁFICOS DE BAIXO: PIZZA (STATUS) + BARRAS (EMPRESA/FILA)
# =====================================================================
g1, g2 = st.columns(2)

# Coluna de status (pra atendida/não atendida)
status_col = None
for cand in ["status", "ds_status", "situacao"]:
    if cand in df.columns:
        status_col = cand
        break

if status_col:
    df_pizza = df.groupby(status_col, as_index=False)["total_ligacoes"].sum()
    fig_pizza = px.pie(
        df_pizza,
        names=status_col,
        values="total_ligacoes",
        title="Atendida x Não Atendida (por status)"
    )
    g1.plotly_chart(fig_pizza, use_container_width=True)

# Barras por Empresa (ou por fila, se existir)
eixo_categoria = "Empresa"
if "fila" in df.columns:
    eixo_categoria = "fila"

df_fila = df.groupby(eixo_categoria, as_index=False)["total_ligacoes"].sum()
fig_fila = px.bar(
    df_fila,
    x="total_ligacoes",
    y=eixo_categoria,
    orientation="h",
    title=f"Total por {eixo_categoria}"
)
g2.plotly_chart(fig_fila, use_container_width=True)

# =====================================================================
# 11) TABELA + DOWNLOAD
# =====================================================================
st.subheader("Tabela de Ligações (amostra)")
st.dataframe(df.head(50))

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Baixar Ligações (CSV)",
    data=csv,
    file_name=f"ligacoes_{usuario}.csv",
    mime="text/csv",
)
