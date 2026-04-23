import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة
st.set_page_config(page_title="REVO 💬", page_icon="💬", layout="centered")

# --- 2. CSS متطور للفقاعات والزخرفة ---
st.markdown("""
    <style>
    .revo-title {
        font-family: 'Courier New', Courier, monospace;
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #128C7E;
        margin-bottom: 20px;
    }
    .chat-bubble {
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
        font-family: sans-serif;
        box-shadow: 0px 1px 1px rgba(0,0,0,0.1);
    }
    .user-bubble { background-color: #DCF8C6; margin-left: auto; border-bottom-right-radius: 2px; }
    .other-bubble { background-color: #FFFFFF; margin-right: auto; border-bottom-left-radius: 2px; border: 1px solid #E5E5E5; }
    
    /* ستايل زر الزائد */
    .plus-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f0f2f5;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        font-size: 24px;
        color: #54656f;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="revo-title">💬 ℛℰ𝒱𝒪 💬</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. منطقة المحادثة ---
user_name = st.sidebar.text_input("سميتك:", value="أحمد")

for msg in st.session_state.messages:
    is_me = msg["user"] == user_name
    bubble_class = "user-bubble" if is_me else "other-bubble"
    st.markdown(f'<div class="chat-bubble {bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg:
        if msg["type"] == "audio": st.audio(msg["file"])
        elif msg["type"] == "image": st.image(msg["file"])
        elif msg["type"] == "video": st.video(msg["file"])

# --- 4. شريط الأدوات السفلي (الزائد + الكتابة) ---
st.write("---")
# غنصاوبو جوج أعمدة: واحد صغير للزائد وواحد كبير للكتابة
cols = st.columns([1, 10])

with cols[0]:
    # زر الزائد لفتح القائمة
    if st.button("➕", help="إرسال وسائط"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

# إيلا تضغط على الزائد، كتبان هاد القائمة (Pop-up Menu)
if st.session_state.get('show_menu', False):
    with st.expander("📎 قائمة الوسائط", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            img_file = st.file_uploader("🖼️ صورة/فيديو", type=["jpg", "png", "mp4"])
        with col2:
            st.write("🎤 أوديو")
            audio = mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='media_mic')
        with col3:
            contact = st.file_uploader("👤 كونتيكت", type=["vcf"])
            cam = st.camera_input("📸 كاميرا") # فتح الكاميرا مباشرة

        if st.button("إرسال المحدّد"):
            if img_file:
                m_type = "image" if img_file.type.startswith("image") else "video"
                st.session_state.messages.append({"user": user_name, "text": f"صيفط {m_type}", "file": img_file.getvalue(), "type": m_type})
            if audio:
                st.session_state.messages.append({"user": user_name, "text": "🎙️ أوديو", "file": audio['bytes'], "type": "audio"})
            if cam:
                st.session_state.messages.append({"user": user_name, "text": "📸 صورة من الكاميرا", "file": cam.getvalue(), "type": "image"})
            
            st.session_state.show_menu = False
            st.rerun()

with cols[1]:
    if prompt := st.chat_input("اكتب رسالة..."):
        st.session_state.messages.append({"user": user_name, "text": prompt})
        st.rerun()