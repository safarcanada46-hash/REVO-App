import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة
st.set_page_config(page_title="REVO 💬", page_icon="💬", layout="centered")

# --- 2. CSS احترافي للتصميم والألوان ---
st.markdown("""
    <style>
    /* تكبير عنوان التطبيق */
    .revo-title {
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 70px; /* حجم كبير جداً */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #128C7E, #075E54);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -20px;
        margin-bottom: 30px;
        letter-spacing: 5px;
    }

    /* تحسين شكل حاوية الميكروفون فوق السهم */
    .mic-container {
        position: fixed;
        bottom: 85px; /* يجي فوق الخانة بالضبط */
        right: 40px;  /* محاذاة مع جهة السهم */
        z-index: 1000;
        background-color: #128C7E;
        border-radius: 50%;
        padding: 5px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    /* ألوان الخلفية والفقاعات */
    .stApp {
        background: linear-gradient(135deg, #f0f2f5, #e5ddd5);
    }
    .user-bubble { 
        background-color: #DCF8C6; 
        padding: 12px; 
        border-radius: 15px 15px 2px 15px; 
        margin-left: auto; 
        width: fit-content; 
        max-width: 80%; 
        margin-bottom: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# عرض العنوان بحجم كبير
st.markdown('<p class="revo-title">REVO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["user"] == "أحمد" else "other-bubble"
    st.markdown(f'<div class="{bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg:
        st.audio(msg["file"])

# --- 3. منطقة الإدخال الذكية ---

# الميكروفون موضوع فوق السهم بالضبط
st.markdown('<div class="mic-container">', unsafe_allow_html=True)
audio_record = mic_recorder(
    start_prompt="🎤", 
    stop_prompt="✅", 
    key='recorder'
)
st.markdown('</div>', unsafe_allow_html=True)

if audio_record:
    st.session_state.messages.append({
        "user": "أحمد", 
        "text": "🎙️ رسالة صوتية", 
        "file": audio_record['bytes']
    })
    st.rerun()

# خانة الكتابة الأساسية (فيها السهم ديالها)
prompt = st.chat_input("اكتب رسالة...")
if prompt:
    st.session_state.messages.append({"user": "أحمد", "text": prompt})
    st.rerun()
