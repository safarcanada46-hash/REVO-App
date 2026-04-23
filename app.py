import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. Page Configuration
st.set_page_config(page_title="DooVoo 💬", page_icon="💬", layout="wide")

# --- 2. Sidebar for Customization (Still active but themed) ---
with st.sidebar:
    st.markdown("### 🎨 Appearance")
    theme_choice = st.selectbox(
        "Select Background:",
        ["Vantablack", "Deep Space", "Midnight Blue"]
    )
    
    # Theme colors
    if theme_choice == "Vantablack":
        bg_color = "#000000" # Absolute Black
        text_color = "#ffffff"
    elif theme_choice == "Deep Space":
        bg_color = "#050505"
        text_color = "#eeeeee"
    else:
        bg_color = "#0a0a0b"
        text_color = "#dddddd"

# --- 3. CSS (Instagram Font + Vantablack Style) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Grand+Hotel&display=swap');

    /* Vantablack Background */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* DooVoo Title (Instagram Style) */
    .doovoo-title {{
        font-family: 'Grand Hotel', cursive;
        font-size: 150px; /* Even bigger as requested */
        text-align: center;
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -80px;
        margin-bottom: 30px;
    }}

    /* Chat Bubbles */
    .user-bubble {{ 
        background-color: #005c4b; /* Dark WhatsApp Green */
        color: white;
        padding: 15px; 
        border-radius: 20px 20px 5px 20px; 
        margin-left: auto; width: fit-content; max-width: 70%; margin-bottom: 12px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }}
    
    /* Input Area Styling */
    .stChatInput {{
        background-color: #1a1a1a !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Display Big DooVoo Title
st.markdown('<p class="doovoo-title">DooVoo</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Conversation
for msg in st.session_state.messages:
    bubble_class = "user-bubble" # All messages as user for now
    st.markdown(f'<div class="{bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg:
        st.audio(msg["file"])

# --- 4. Input Area (English Labels) ---
st.write("---")
cols = st.columns([0.6, 0.6, 8])

with cols[0]:
    if st.button("➕", key="plus"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

with cols[1]:
    audio_record = mic_recorder(start_prompt="🎤", stop_prompt="✅", key='recorder')

with cols[2]:
    prompt = st.chat_input("Type a message...")
    if prompt:
        st.session_state.messages.append({"user": "Ahmad", "text": prompt})
        st.rerun()

# Audio Handling
if audio_record:
    st.session_state.messages.append({"user": "Ahmad", "text": "🎙️ Voice Message", "file": audio_record['bytes']})
    st.rerun()

# Media Menu
if st.session_state.get('show_menu', False):
    with st.expander("📎 Attachments", expanded=True):
        st.camera_input("Take a Photo")
        st.file_uploader("Upload File")
