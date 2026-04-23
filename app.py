import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة
st.set_page_config(page_title="REVO 💬", page_icon="💬", layout="wide")

# --- 2. اختيار الألوان من الجنب (Sidebar) ---
with st.sidebar:
    st.markdown("### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox(
        "اختار لون الخلفية:",
        ["الأخضر الهادئ", "الأزرق السماوي", "الوردي الناعم", "الأصفر المشرق", "الذهبي"]
    )
    
    colors = {
        "الأخضر الهادئ": "linear-gradient(135deg, #e8f5e9, #c8e6c9)",
        "الأزرق السماوي": "linear-gradient(135deg, #e3f2fd, #bbdefb)",
        "الوردي الناعم": "linear-gradient(135deg, #fce4ec, #f8bbd0)",
        "الأصفر المشرق": "linear-gradient(135deg, #fffde7, #fff9c4)",
        "الذهبي": "linear-gradient(135deg, #fff9c4, #ffecb3)"
    }
    bg_gradient = colors.get(theme_choice)

# --- 3. CSS (استيراد خط Instagram + التصميم) ---
st.markdown(f"""
    <style>
    /* استيراد الخط اللي كيشبه لـ Instagram */
    @import url('https://fonts.googleapis.com/css2?family=Grand+Hotel&display=swap');

    .stApp {{
        background: {bg_gradient};
    }}

    /* ستايل العنوان بحال Instagram */
    .revo-title {{
        font-family: 'Grand Hotel', cursive;
        font-size: 100px; /* حجم كبير وواضح */
        text-align: center;
        color: #262626; /* لون غامق كلاسيكي */
        margin-top: -60px;
        margin-bottom: 20px;
        font-weight: normal;
    }}

    .user-bubble {{ 
        background-color: #DCF8C6; padding: 12px; border-radius: 15px 15px 2px 15px; 
        margin-left: auto; width: fit-content; max-width: 70%; margin-bottom: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# عرض العنوان بستايل Instagram
st.markdown('<p class="revo-title">Revo</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["user"] == "أحمد" else "other-bubble"
    st.markdown(f'<div class="{bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg:
        st.audio(msg["file"])

# --- 4. منطقة الإدخال (الزائد والأوديو والرسالة) ---
st.write("---")
cols = st.columns([0.6, 0.6, 8])

with cols[0]:
    if st.button("➕", key="plus"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

with cols[1]:
    audio_record = mic_recorder(start_prompt="🎤", stop_prompt="✅", key='recorder')

with cols[2]:
    prompt = st.chat_input("اكتب رسالة...")
    if prompt:
        st.session_state.messages.append({"user": "أحمد", "text": prompt})
        st.rerun()

if audio_record:
    st.session_state.messages.append({"user": "أحمد", "text": "🎙️ رسالة صوتية", "file": audio_record['bytes']})
    st.rerun()

if st.session_state.get('show_menu', False):
    with st.expander("📎 وسائط", expanded=True):
        st.camera_input("📸 صورة")
        st.file_uploader("📁 ملف")
