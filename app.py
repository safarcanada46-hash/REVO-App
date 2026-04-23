import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة والتصميم
st.set_page_config(page_title="REVO 💬", page_icon="💬", layout="centered")

# --- 2. CSS متطور لإخفاء السهم وتحسين الواجهة ---
st.markdown("""
    <style>
    /* إخفاء زر السهم الافتراضي داخل chat_input */
    button[data-testid="stChatInputSubmit"] {
        display: none !important;
    }
    
    .revo-title {
        font-family: 'Courier New', Courier, monospace;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #128C7E;
        margin-bottom: 20px;
    }
    
    /* ستايل فقاعات الشات */
    .user-bubble { background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-left: auto; width: fit-content; max-width: 80%; margin-bottom: 10px; }
    .other-bubble { background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin-right: auto; width: fit-content; max-width: 80%; border: 1px solid #E5E5E5; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="revo-title">💬 ℛℰ𝒱𝒪 💬</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["user"] == "أحمد" else "other-bubble"
    st.markdown(f'<div class="{bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg: st.audio(msg["file"])

# --- 3. شريط الأدوات السفلي (الواتساب ستايل) ---
st.write("---")
# غادي نقسمو لتحت لـ 3 أعمدة: الزائد، خانة الكتابة، والميكروفون
bottom_cols = st.columns([1, 8, 1])

with bottom_cols[0]:
    if st.button("➕", key="plus"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

with bottom_cols[1]:
    # خانة الكتابة (السهم مخفي دابا بـ CSS)
    prompt = st.chat_input("اكتب رسالة...")
    if prompt:
        st.session_state.messages.append({"user": "أحمد", "text": prompt})
        st.rerun()

with bottom_cols[2]:
    # الميكروفون في مكان السهم تماماً
    audio_record = mic_recorder(
        start_prompt="🎤", 
        stop_prompt="✅", 
        key='recorder'
    )
    if audio_record:
        st.session_state.messages.append({
            "user": "أحمد", 
            "text": "🎙️ رسالة صوتية", 
            "file": audio_record['bytes'], 
            "type": "audio"
        })
        st.rerun()

# قائمة الوسائط (إيلا تضغط على الزائد)
if st.session_state.get('show_menu', False):
    with st.expander("📎 وسائط إضافية", expanded=True):
        st.camera_input("📸 صور دابا")
        st.file_uploader("📁 ملفات")
