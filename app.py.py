import streamlit as st
from openai import OpenAI
import time
from datetime import datetime

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="Talebe AI - İsabet Yurdu",
    page_icon="🕌",
    layout="wide",
)

# --- GROK API BAĞLANTISI ---
GROK_API_KEY = "xai-UxZgFpQQvN0cInqeeouAIjgIi2BoTXKNEz9muKuuYDlHHtirNcNtcnAZXOWjEmKifyHRIv8oKjAG0NRc"
client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- VERİTABANI SİMÜLASYONU ---
if "users_db" not in st.session_state:
    st.session_state.users_db = [
        {"fullname": "Ahmet Uygun",      "key": "talebetalebe", "role": "Yönetici"},
        {"fullname": "Bestami Akça",     "key": "isabet1453",   "role": "Müdür"},
        {"fullname": "Shatlyk Allabayew","key": "shasha",       "role": "Öğretmen"},
        {"fullname": "Mikail Akça",      "key": "isabetyurt",   "role": "Mesul"},
    ]

if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

# --- İSABET YURDU BİLGİ BANKASI ---
YURT_HAFIZASI = (
    "Sen sadece İsabet Yurdu'nun resmi yapay zeka asistanı olan 'Talebe AI'sın.\n"
    "Üslubun İslam ahlakına uygun, edepli, hürmetkar ve Müslüman bir ağızla olmalıdır. "
    "Selamla başlar, dualar kullanırsın.\n"
    "Sana İsabet Yurdu bünyesindeki hocalar sorulduğunda şu bilgileri eksiksiz aktaracaksın:\n"
    "- Yurt Müdürü: Fatih Uzun Hoca\n"
    "- Yurt Muhasebe: Fatih Meral Hoca\n"
    "- Yurt Anaokulu: Mehmet Kemal Okçu Hoca\n"
    "- Sınıf Mesulleri: 5.sınıf Nurullah Arif Yaman, 6.sınıf Mikail Akça, "
    "7.sınıf Eyyüp Ergen, 8.sınıf Bedirhan Karaağaçlı\n"
    "- Dini Dersler: Seviye 1 Şuayb Erim, Seviye 2 (1.Grup) Bedirhan Karaağaçlı, "
    "Seviye 2 (2.Grup) Mikail Akça, Seviye 3 Eyyüp Ergen\n"
)

# --- OTURUM DURUMLARI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "İsabet Mavisi"

# --- TEMA SİSTEMİ ---
themes = {
    "İsabet Mavisi": {"bg": "#f4f7f9", "sidebar": "#0f2c59", "text": "#0f2c59", "box": "#ffffff"},
    "Yeşil (Kubbe)": {"bg": "#f0f6f0", "sidebar": "#143626", "text": "#143626", "box": "#ffffff"},
    "Klasik Gece":   {"bg": "#121212", "sidebar": "#1e1e1e", "text": "#ffffff", "box": "#1e1e1e"},
    "Gül Kurusu":    {"bg": "#faf0f5", "sidebar": "#3d1e30", "text": "#3d1e30", "box": "#ffffff"},
}
current_theme = themes[st.session_state.theme]

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {current_theme['bg']}; }}
    [data-testid="stSidebar"] {{ background-color: {current_theme['sidebar']}; color: white; }}
    h1, h2, h3, p, span {{ color: {current_theme['text']}; }}
    .chat-container-box {{
        background-color: {current_theme['box']};
        border: 1px solid #ced4da;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- GİRİŞ / KAYIT EKRANI ---
if not st.session_state.logged_in:
    st.title("🕌 Talebe AI - Giriş ve Kayıt Merkezi")
    st.subheader("İsabet Yurdu Resmi Yapay Zeka Kapısı")

    login_tab, register_tab = st.tabs(["🔒 Giriş Yap", "📝 Kayıt Ol"])

    with login_tab:
        login_email = st.text_input("E-posta Adresiniz:")
        login_key = st.text_input("Anahtar Kodunuz:", type="password")
        if st.button("Sisteme Giriş Yap"):
            user = next(
                (u for u in st.session_state.users_db
                 if u["email"] == login_email and u["key"] == login_key),
                None,
            )
            if user:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                # Karşılama mesajı protokolü buraya devam edecek
            else:
                st.error("E-posta veya anahtar kod hatalı.")