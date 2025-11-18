import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Login - Sonax In Home", layout="wide")

BASE_DIR = Path(__file__).resolve().parent


USERS = {
    "ALESSANDRA SOUZA": {"senha": "1234", "alias": 309},
    "AMANDA MARIANO": {"senha": "1234", "alias": 504},
    # ... (complete com os demais usuários)
}

# =====================================================================
# CSS – fundo branco, layout centralizado, botão preto
# =====================================================================
st.markdown("""
<style>
html, body, .stApp {
    height: 100%;
    margin: 0;
    padding: 0;
    background-color: #ffffff !important;
}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh !important;
}
.login-box {
    background-color: #ffffff;
    padding: 40px 30px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    width: 320px;
    text-align: center;
}
.login-box .stImage img {
    width: 130px;
    margin-bottom: 50px;
}
.login-title {
    font-size: 28px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 8px;
}
.login-subtitle {
    font-size: 14px;
    color: #000000;
    margin-bottom: 25px;
}
.stTextInput label {
    color: #000 !important;
    font-weight: 600;
}
.stTextInput > div > div > input {
    height: 40px;
    border-radius: 8px;
    font-size: 14px;
}
.stButton>button {
    width: 100%;
    background: #000000 !important;
    color: #ffffff !important;
    font-size: 15px;
    font-weight: bold;
    padding: 10px;
    border-radius: 999px;
    border: none;
    margin-top: 10px;
}
.stButton>button:hover {
    filter: brightness(1.1);
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# Redirecionamento se já estiver logado
# =====================================================================
if "usuario" in st.session_state and "alias" in st.session_state:
    try:
        st.switch_page("pages/01_Dashboard.py")
    except Exception:
        pass

# =====================================================================
# Layout da tela de login
# =====================================================================
st.markdown("<div class='login-box'>", unsafe_allow_html=True)



st.markdown("<div class='login-title'>Entrar</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='login-subtitle'>Acesse o painel da Sonax In Home com seu usuário e senha.</div>",
    unsafe_allow_html=True
)

with st.form("login_form"):
    user = st.text_input("Email")
    pwd = st.text_input("Password", type="password")
    ok = st.form_submit_button("Login")

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# Autenticação
# =====================================================================
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