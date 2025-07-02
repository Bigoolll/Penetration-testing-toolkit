import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Offensive Security Toolkit", layout="centered")

# Page CSS for nice big buttons
st.markdown("""
    <style>
    .big-button {
        display: block;
        background: linear-gradient(135deg, #0f3460, #1e5f74);
        color: white;
        padding: 25px 40px;
        margin: 20px auto;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        cursor: pointer;
        text-decoration: none;
        width: 50%;
    }
    .big-button:hover {
        background: linear-gradient(135deg, #1e5f74, #0f3460);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center; color: #00d4ff;">All-in-One Offensive Security Toolkit</h1>', unsafe_allow_html=True)

st.markdown('<h7 style="text-align: left;">A simple, customizable toolkit designed for educational penetration testing purposes. This toolkit includes various tools to simulate attacks and gather information on networks, helping users understand security vulnerabilities and learn offensive security techniques.</p>', unsafe_allow_html=True)

st.markdown('<h3 style="text-align: center; color: #00d4ff;">Key Features</h4>', unsafe_allow_html=True)

st.markdown('<h7 style="text-align: left;"> <ul style="text-align: left; font-size: 18px;"> <li><b>DoS Attack Tool:</b> Simulate denial-of-service attacks to stress-test systems.</li> <li><b>Port Scanner:</b> Scan for open ports on a target IP.</li> <li><b>Directory Enumerator:</b> Discover accessible directories on web servers.</li> <li><b>Brute Forcing Tool:</b> Test password strength on common protocols.</li> </ul></p>', unsafe_allow_html=True)