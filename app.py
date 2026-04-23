import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة
st.set_page_config(page_title="REVO 💬", page_icon="💬", layout="centered")

# --- 2. إضافة اختيار الألوان في الجنب (Sidebar) ---
with st.sidebar:
    st.markdown("### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox(
        "اختار لون الخلفية:",
        ["الأخضر الهادئ", "الأزرق السماوي", "الوردي الناعم", "الأصفر المشرق", "الذهبي"]
    )
    
    if theme_choice == "الأخضر الهادئ":
        bg_gradient = "linear-gradient(135deg, #e8f5e9, #c8e6c9)"
    elif theme_choice == "الأزرق السماوي":
        bg_gradient = "linear-gradient(135deg, #e3f2fd, #bbdefb)"
    elif theme_choice == "الوردي الناعم":
        bg_gradient = "linear-gradient(135deg, #fce4ec, #f8bbd0)"
    elif theme_choice == "الأصفر المشرق":
        bg_gradient = "linear-gradient(135deg, #fffde7, #fff9c4)"
    else:
        bg_gradient = "linear-gradient(135deg, #fff9c4, #ffecb3)"

# --- 3. CSS للتصميم العام وتكبير السمية ---
st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_gradient};
    }}
    .revo-title {{
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 75px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #128C7E, #075E54);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -30px;
        margin-bottom: 20px;
    }}
    .user-bubble {{ 
        background-color: #DCF8C6; 
        padding: 12px; 
        border-radius: 15px 15px 2px 15px; 
        margin-left: auto; 
        width: fit-content; 
        max-width: 80%; 
        margin-bottom: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="revo-title">REVO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["user"] == "أحمد" else "other-bubble"
    st.markdown(f'<div class="{bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg:
        st.audio(msg["file"])

# --- 4. شريط الأدوات السفلي (الزائد والأوديو حدا بعضياتهم) ---
st.write("---")
# تقسيم السطر: عمود لـ (+) وعمود لـ (🎤) وعمود كبير للكتابة
input_cols = st.columns([0.8, 0.8, 8])

with input_cols[0]:
    if st.button("➕", key="plus_btn"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

with input_cols[1]:
    # زر الأوديو في جنب الزائد بالضبط
    audio_record = mic_recorder(
        start_prompt="🎤", 
        stop_prompt="✅", 
        key='recorder'
    )

with input_cols[2]:
    prompt = st.chat_input("اكتب رسالة...")
    if prompt:
        st.session_state.messages.append({"user": "أحمد", "text": prompt})
        st.rerun()

# معالجة الأوديو إيلا تسجل
if audio_record:
    st.session_state.messages.append({
        "user": "أحمد", 
        "text": "🎙️ رسالة صوتية", 
        "file": audio_record['bytes']
    })
    st.rerun()

# منيو الوسائط إيلا تضغط الزائد
if st.session_state.get('show_menu', False):
    with st.expander("📎 وسائط", expanded=True):
        st.camera_input("📸 صورة سريعة")
        st.file_uploader("📁 ملف")
