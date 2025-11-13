import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import subprocess
import sys

APP_BUILD = "2025-11-12-18h3"
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
    """Chama o script atualiza_dados.py passando alias + nome do usuário logado."""
    with st.spinner("Buscando dados diretamente na API... isso pode demorar ⏳"):
        user = st.session_state.get("usuario")
        alias = st.session_state.get("alias")
        args = [sys.executable, "atualiza_dados.py", "--alias", str(alias), "--dias", "30"]
        if user:
            args += ["--nome", str(user)]
        # para debugar local: args += ["--debug"]
        subprocess.run(args, cwd=str(BASE_DIR))
    st.success("Atualização concluída! Os arquivos locais foram atualizados. ✅")


# =====================================================================
# 3) ESTILO GLOBAL
# =====================================================================
st.markdown(
    """
<style>
* {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, 'Helvetica Neue', Arial,
               'Noto Sans', 'Liberation Sans', 'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol' !important;
}

/* esconder menu padrão */
header, #MainMenu, footer { visibility: hidden; height: 0; }

/* sidebar clarinha */
section[data-testid="stSidebar"] {
  background: #f5f2ec;
}

/* fundo geral branco */
html, body, .stApp {
  background-color: #ffffff !important;
  color: #111 !important;
}

/* título padrão */
h1 {
  font-weight: 800 !important;
  letter-spacing: 0.3px;
  color: #111 !important;
}

/* container fullpage só pra tela de login */
.fullpage-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
}

/* card de login */
.login-card {
  border: 1px solid rgba(0,0,0,0.06);
  background: #faf9f7;
  border-radius: 12px;
  padding: 24px 22px 18px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

/* inputs */
.stTextInput > div > div > input {
  background: #fff !important;
  border: 1px solid #ccc !important;
  height: 42px;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 15px;
  color: #111 !important;
}

/* foco inputs */
.stTextInput > div > div:focus-within {
  border-color: #2687e2 !important;
  box-shadow: 0 0 0 2px rgba(38,135,226,0.25) !important;
}

/* botão principal: azul */
.stButton>button {
  background: #2687e2 !important;
  border: 0 !important;
  color: #fff !important;
  font-weight: 700 !important;
  padding: 8px 18px !important;
  border-radius: 8px !important;
}
.stButton>button:hover {
  filter: brightness(1.05);
}

/* logo no topo centralizada */
img[alt="Sonax Logo"], img[alt="logo"] {
  display: block;
  margin-left: auto !important;
  margin-right: auto !important;
  margin-top: 10px;
  margin-bottom: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)

LOGO = BASE_DIR / "assets" / "logo_sonax.png"
IMG_SIDE = BASE_DIR / "assets" / "login_side.png"   # sua imagem do foguete

# =====================================================================
# 3.1) TELA DE LOGIN (FIXA, 2 COLUNAS)
# =====================================================================
if "usuario" not in st.session_state:

    st.markdown('<div class="fullpage-login">', unsafe_allow_html=True)

    colL, colR = st.columns([0.48, 0.52])

    # ------------------ COLUNA ESQUERDA: logo + formulário ------------------
    with colL:
        if LOGO.exists():
            st.image(str(LOGO), caption=None, use_column_width=False, width=220)
        st.markdown(
            "### Acesse seu painel\n"
            "Veja suas ligações, atendimentos e desempenho em um só lugar."
        )

        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            user = st.text_input("Usuário", key="login_user")
            pwd = st.text_input("Senha", type="password", key="login_pwd")
            entrou = st.form_submit_button("Acessar")

        st.markdown("</div>", unsafe_allow_html=True)

        if entrou:
            if user in USERS and USERS[user]["senha"] == pwd:
                st.session_state["usuario"] = user
                st.session_state["alias"] = USERS[user]["alias"]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    # ------------------ COLUNA DIREITA: imagem lateral ------------------
    with colR:
        if IMG_SIDE.exists():
            st.image(str(IMG_SIDE), use_column_width=True)
        else:
            st.write("")  # vazio, se não tiver imagem

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =====================================================================
# 4) PÓS-LOGIN (DASHBOARD)
# =====================================================================
usuario = st.session_state["usuario"]
alias = st.session_state["alias"]

st.title("Dashboard de Ligações - Agentes")
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
# 6) FILTROS BÁSICOS (ano/mês)
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
    fig_linha = px.line(
        df_linha,
        x="dia",
        y="total_ligacoes",
        title="Ligações por Dia",
        markers=True,
    )
    fig_linha.update_traces(
        line=dict(color="#46a049", width=3),
        fill="tozeroy",
        fillcolor="rgba(70,160,73,0.2)",
        text=df_linha["total_ligacoes"],
        texttemplate="<b>%{text}</b>",
        textposition="top center",
    )
    fig_linha.update_layout(
        xaxis_title="Dia",
        yaxis_title="Total de ligações",
        hovermode="x unified",
        yaxis=dict(rangemode="tozero"),
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
    atendidas_set = {"OK", "ATENDIDA", "ATENDIDAS", "ATENDIMENTO", "COMPLETED"}
    tmp = df[[status_col, "total_ligacoes"]].copy()
    tmp["__norm"] = tmp[status_col].astype(str).str.upper().str.strip()
    tmp["Status"] = tmp["__norm"].apply(
        lambda s: "Atendidas" if s in atendidas_set else "Não atendidas"
    )

    df_status = tmp.groupby("Status", as_index=False)["total_ligacoes"].sum()
    df_status["Status"] = pd.Categorical(
        df_status["Status"],
        categories=["Atendidas", "Não atendidas"],
        ordered=True,
    )
    df_status = df_status.sort_values("Status")

    color_map = {"Atendidas": "#46a049", "Não atendidas": "#f19a37"}
    fig_pizza = px.pie(
        df_status,
        names="Status",
        values="total_ligacoes",
        title="Atendidas x Não Atendidas",
        color="Status",
        color_discrete_map=color_map,
    )
    fig_pizza.update_traces(textinfo="label+value+percent")
    g1.plotly_chart(fig_pizza, use_container_width=True)

# --- BARRAS HORIZONTAIS ---
eixo_categoria = "Empresa" if "Empresa" in df.columns else None
if "fila" in df.columns:
    eixo_categoria = "fila"

if eixo_categoria:
    df_fila = (
        df.groupby(eixo_categoria, as_index=False)["total_ligacoes"]
        .sum()
        .sort_values("total_ligacoes")
    )
    fig_fila = px.bar(
        df_fila,
        x="total_ligacoes",
        y=eixo_categoria,
        orientation="h",
        title=f"Total por {eixo_categoria}",
    )
    fig_fila.update_traces(
        marker_color="#f19a37",
        marker_line_color="black",
        marker_line_width=1,
        text=df_fila["total_ligacoes"],
        texttemplate="%{text}",
        textposition="outside",
    )
    fig_fila.update_layout(
        xaxis_title="Total de ligações",
        yaxis_title=eixo_categoria,
        uniformtext_minsize=10,
        uniformtext_mode="show",
        margin=dict(l=10, r=10, t=60, b=10),
        yaxis=dict(automargin=True),
        xaxis=dict(rangemode="tozero"),
    )
    g2.plotly_chart(fig_fila, use_container_width=True)

# =====================================================================
# 10) DIAGNÓSTICO RÁPIDO
# =====================================================================
with st.expander("Diagnóstico rápido (contagem por empresa e dia da semana)"):
    if "Empresa" in df.columns:
        diag = (
            df.assign(DiaSemana=df["dt_inicio"].dt.dayofweek)  # 0=Seg ... 6=Dom
            .groupby(["Empresa", "DiaSemana"], as_index=False)["total_ligacoes"]
            .sum()
            .sort_values(["Empresa", "DiaSemana"])
        )
        nomes = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}
        diag["DiaSemana"] = diag["DiaSemana"].map(nomes)
        st.dataframe(diag, use_container_width=True)
    else:
        st.info("Coluna 'Empresa' não encontrada no dataset.")

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
