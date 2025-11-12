import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import subprocess
import sys

APP_BUILD = "2025-11-12-18h"
st.set_page_config(page_title="Dashboard de Ligações", layout="wide")
st.caption(f"Build: {APP_BUILD}")

# =====================================================================
# 0) DIRETÓRIOS / ARQUIVOS
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)

# =====================================================================
# 1) CONFIGURAÇÃO DE USUÁRIOS (LOGIN -> ALIAS)
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
        subprocess.run([sys.executable, "atualiza_dados.py"], cwd=str(BASE_DIR))
    st.success("Atualização concluída! Os arquivos locais foram atualizados. ✅")

# =====================================================================
# 3) ESTILO / LOGIN
# =====================================================================
st.markdown("""
<style>
/* =================== RESET GERAL =================== */
* {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Liberation Sans', 'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol' !important;
}
header, #MainMenu, footer { visibility: hidden; height: 0; }
section[data-testid="stSidebar"] { background: #f5f2ec; }

/* Fundo geral e cor do texto */
html, body, .stApp {
  background-color: #f5f2ec !important;
  color: #111 !important;
}

/* =================== TÍTULO =================== */
h1, .st-emotion-cache-10trblm {
  font-weight: 800 !important;
  letter-spacing: 0.3px;
  color: #111 !important;
}

/* =================== CARD DE LOGIN =================== */
.login-card {
  border: 1px solid rgba(0,0,0,0.08);
  background: #faf9f7;
  border-radius: 12px;
  padding: 22px 20px 16px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

/* =================== INPUTS =================== */
.stTextInput > div > div > input {
  background: #fff !important;
  border: 1px solid #bbb !important;
  color: #111 !important;
}
.stTextInput > div > div:focus-within {
  border-color: #46a049 !important;
  box-shadow: 0 0 0 2px rgba(70,160,73,0.2);
}

/* =================== BOTÃO =================== */
.stButton>button {
  background: #46a049 !important;
  border: 0 !important;
  color: #fff !important;
  font-weight: 700;
  padding: 8px 18px;
  border-radius: 8px;
}
.stButton>button:hover { filter: brightness(1.05); }

/* =================== LOGO =================== */
img[alt="Sonax Logo"], img[alt="logo"] {
  display: block;
  margin-left: auto !important;
  margin-right: auto !important;
  margin-top: 30px;
  margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


LOGO = BASE_DIR / "assets" / "logo_sonax.png"
st.title("Dashboard de Ligações - Agentes")

# ---- LOGIN estilizado (único) ----
if "usuario" not in st.session_state:
    colL, colSpacer, colR = st.columns([0.58, 0.02, 0.40])
    with colL:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        with st.form("login", clear_on_submit=False):
            user = st.text_input("Usuário", key="login_user")
            colps, colchk = st.columns([0.86, 0.14])
            with colps:
                pwd = st.text_input("Senha", type="password", key="login_pwd")
            with colchk:
                mostrar = st.checkbox("👁", value=False, help="Mostrar senha")
            if mostrar:
                st.info(pwd if pwd else "Digite a senha...", icon="🔑")
            entrou = st.form_submit_button("Entrar")
        st.markdown('</div>', unsafe_allow_html=True)

        if LOGO.exists():
            st.markdown('<div class="container-tight"></div>', unsafe_allow_html=True)
            st.image(str(LOGO), use_column_width=False, width=520)
        else:
            st.caption("Logo não encontrada em assets/logo_sonax.png")

    # coluna direita sem mascote (opcional)

    if entrou:
        if user in USERS and USERS[user]["senha"] == pwd:
            st.session_state["usuario"] = user
            st.session_state["alias"] = USERS[user]["alias"]
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.stop()

# =====================================================================
# 4) PÓS-LOGIN (DASHBOARD)
# =====================================================================
# Botão de logout (útil para testar a tela de login)
with st.sidebar:
    if st.button("↩️ Sair"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

usuario = st.session_state["usuario"]
alias = st.session_state["alias"]
st.subheader(f"Agente: {usuario} (alias {alias})")

if st.button("🔄 Atualizar Agora"):
    atualizar_agora()

df = carregar_dados_local(alias)
if df is None or df.empty:
    st.stop()

# =====================================================================
# 5) PREPARAÇÃO DOS DADOS
# =====================================================================
if "dt_inicio" in df.columns:
    df["dt_inicio"] = pd.to_datetime(df["dt_inicio"], dayfirst=True, errors="coerce")
else:
    st.error("Coluna 'dt_inicio' não encontrada nos dados. Verifique o arquivo gerado.")
    st.stop()

df["dia"] = df["dt_inicio"].dt.day
df["mes"] = df["dt_inicio"].dt.month
df["ano"] = df["dt_inicio"].dt.year
if "total_ligacoes" not in df.columns:
    df["total_ligacoes"] = 1

# =====================================================================
# 6) FILTROS
# =====================================================================
anos_disponiveis = sorted(df["ano"].dropna().unique())
meses_nomes = ["janeiro","fevereiro","março","abril","maio","junho",
               "julho","agosto","setembro","outubro","novembro","dezembro"]
mes_map = {nome: i + 1 for i, nome in enumerate(meses_nomes)}

col_f1, col_f2 = st.columns(2)
with col_f1:
    ano_opcoes = ["Todos"] + [int(a) for a in anos_disponiveis]
    ano_sel = st.selectbox("Filtro Ano", ano_opcoes)
with col_f2:
    mes_sel = st.selectbox("Filtro Mês", ["Todos"] + meses_nomes)

if ano_sel != "Todos":
    df = df[df["ano"] == int(ano_sel)]
if mes_sel != "Todos":
    df = df[df["mes"] == mes_map[mes_sel]]

if df.empty:
    st.warning("Nenhum dado após aplicar os filtros selecionados.")
    st.stop()

# =====================================================================
# 7) MÉTRICAS
# =====================================================================
total_ligacoes = int(df["total_ligacoes"].sum())
total_empresas = df["Empresa"].nunique() if "Empresa" in df.columns else 0
m1, m2 = st.columns(2)
with m1:
    st.metric("Total Empresas", total_empresas)
with m2:
    st.metric("Total Ligações", f"{total_ligacoes:,}".replace(",", "."))

# =====================================================================
# 8) GRÁFICO LINHA: LIGAÇÕES POR DIA
# =====================================================================
if "dia" in df.columns:
    df_linha = df.groupby("dia", as_index=False)["total_ligacoes"].sum().sort_values("dia")
    fig_linha = px.line(df_linha, x="dia", y="total_ligacoes", title="Ligações por Dia", markers=True)
    fig_linha.update_traces(
        line=dict(color="#46a049", width=3),
        fill="tozeroy",
        fillcolor="rgba(70,160,73,0.2)",
        text=df_linha["total_ligacoes"],
        texttemplate="<b>%{text}</b>",
        textposition="top center"
    )
    fig_linha.update_layout(
        xaxis_title="Dia",
        yaxis_title="Total de ligações",
        hovermode="x unified",
        yaxis=dict(rangemode="tozero")
    )
    st.plotly_chart(fig_linha, use_container_width=True)

# =====================================================================
# 9) PIZZA (Atendidas x Não atendidas) + BARRAS HORIZONTAIS
# =====================================================================
g1, g2 = st.columns(2)

# --- PIZZA ---
status_col = None
for cand in ["status", "ds_status", "situacao"]:
    if cand in df.columns:
        status_col = cand
        break

if status_col:
    df_status = df.groupby(status_col, as_index=False)["total_ligacoes"].sum()
    mapa = {
        "OK": "Atendidas", "ATENDIDA": "Atendidas",
        "INDISPONÍVEL": "Não atendidas", "INDISPONIVEL": "Não atendidas",
        "NAO ATENDIDA": "Não atendidas", "NÃO ATENDIDA": "Não atendidas",
    }
    df_status["Status"] = df_status[status_col].astype(str).str.upper().map(mapa).fillna(df_status[status_col])
    ordem = ["Atendidas", "Não atendidas"]
    df_status["Status"] = pd.Categorical(df_status["Status"], categories=ordem, ordered=True)
    df_status = df_status.groupby("Status", as_index=False)["total_ligacoes"].sum()

    color_map = {"Atendidas": "#46a049", "Não atendidas": "#f19a37"}
    fig_pizza = px.pie(
        df_status, names="Status", values="total_ligacoes",
        title="Atendidas x Não Atendidas", color="Status", color_discrete_map=color_map
    )
    fig_pizza.update_traces(
        textinfo="label+value+percent",
        textfont=dict(size=13),
        pull=[0.02 if s == "Não atendidas" else 0 for s in df_status["Status"]]
    )
    g1.plotly_chart(fig_pizza, use_container_width=True)

# --- BARRAS HORIZONTAIS ---
eixo_categoria = "Empresa" if "Empresa" in df.columns else None
if "fila" in df.columns:
    eixo_categoria = "fila"
if eixo_categoria:
    df_fila = df.groupby(eixo_categoria, as_index=False)["total_ligacoes"].sum().sort_values("total_ligacoes")
    fig_fila = px.bar(
        df_fila, x="total_ligacoes", y=eixo_categoria,
        orientation="h", title=f"Total por {eixo_categoria}"
    )
    fig_fila.update_traces(
        marker_color="#f19a37",
        marker_line_color="black",
        marker_line_width=1,
        text=df_fila["total_ligacoes"],
        texttemplate="%{text}",
        textposition="outside"
    )
    fig_fila.update_layout(
        xaxis_title="Total de ligações", yaxis_title=eixo_categoria,
        uniformtext_minsize=10, uniformtext_mode="show",
        margin=dict(l=10, r=10, t=60, b=10),
        yaxis=dict(automargin=True),
        xaxis=dict(rangemode="tozero")
    )
    g2.plotly_chart(fig_fila, use_container_width=True)

# =====================================================================
# 10) TABELA + DOWNLOAD
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
