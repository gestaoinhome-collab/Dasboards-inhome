import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Login - Sonax In Home", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
LOGO = BASE_DIR / "assets" / "logo_sonax.png"

# ============================================================
# 1) USUÁRIOS
# (copiei o seu dicionário inteiro para ficar pronto pra uso)
# ============================================================
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

# ============================================================
# 2) CSS – tudo centralizado no meio da tela
# ============================================================
st.markdown("""
<style>
/* Fundo azul */
body, .stApp {
    background-color: #2687e2 !important;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

/* Container principal centralizado */
.block-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Caixa de login centralizada */
.login-box {
    background-color: #ffffff;
    padding: 40px 30px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    width: 320px;
    text-align: center;
}

/* Logo */
.login-box .stImage img {
    width: 100px;
    margin-bottom: 24px;
}

/* Título e subtítulo */
.login-title {
    font-size: 30px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 6px;
    text-align: center;
}
.login-subtitle {
    font-size: 16px;
    color: #000000;
    margin-bottom: 24px;
    text-align: center;
}

/* Inputs */
.stTextInput label {
    color: #000000 !important;
    font-weight: 600;
}
.stTextInput > div > div > input {
    height: 42px;
    border-radius: 8px;
    font-size: 14px;
}

/* Botão */
.stButton>button {
    width: 100%;
    background: #ffffff !important;
    color: #2687e2 !important;
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    border-radius: 999px;
    border: none;
    margin-top: 8px;
}
.stButton>button:hover {
    filter: brightness(0.95);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3) Se já estiver logado, tenta ir pro dashboard
# ============================================================
if "usuario" in st.session_state and "alias" in st.session_state:
    try:
        st.switch_page("pages/01_Dashboard.py")
    except Exception:
        pass

# ============================================================
# 4) CONTEÚDO DO LOGIN – tudo fica no centro
st.markdown("<div class='login-box'>", unsafe_allow_html=True)

# Logo, título, subtítulo, formulário...
# Exemplo:
st.image(str(LOGO))
st.markdown("<div class='login-title'>Entrar</div>", unsafe_allow_html=True)
st.markdown("<div class='login-subtitle'>Acesse o painel da Sonax In Home com seu usuário e senha.</div>", unsafe_allow_html=True)

with st.form("login_form"):
    user = st.text_input("Email")
    pwd = st.text_input("Password", type="password")
    ok = st.form_submit_button("Login")

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 5) Autenticação
# ============================================================
if ok:
    if user in USERS and USERS[user]["senha"] == pwd:
        st.session_state["usuario"] = user
        st.session_state["alias"] = USERS[user]["alias"]

        try:
            st.switch_page("pages/01_Dashboard.py")
        except Exception:
            st.experimental_rerun()
    else:
        st.error("Usuário ou senha incorretos.")
