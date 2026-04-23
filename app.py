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
    
    # تحديد التدرج اللوني (Gradient) حسب اختيارك
    colors = {
        "الأخضر الهادئ": "linear-gradient(135deg, #e8f5e9, #c8e6c9)",
        "الأزرق السماوي": "linear-gradient(135deg, #e3f2fd, #bbdefb)",
        "الوردي الناعم": "linear-gradient(135deg, #fce4ec, #f8bbd0)",
        "الأصفر المشرق": "linear-gradient(135deg, #fffde7, #fff9c4)",
        "الذهبي": "linear-gradient(135deg, #fff9c4, #ffecb3)"
    }
    bg_gradient = colors.get(theme_choice)

# --- 3. CSS احترافي (تكبير العنوان + ستايل الفقاعات) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_gradient};
    }}
    /* تكبير سمية التطبيق بزاف وتوسيطها */
    .revo-title {{
        font-family: 'Arial Black', sans-serif;
        font-size: 85px; /* حجم ضخم */
        font-weight: 900;
        text-align: center;
        color: #128C7E;
        margin-top: -50px;
        margin-bottom: 40px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
    }}
    .user-bubble {{ 
        background-color: #DCF8C6; padding: 12px; border-radius: 15px 15px 2px 15px; 
        margin-left: auto; width: fit-content; max-width: 70%; margin-bottom: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    /* تحسين شكل أزرار التحكم */
    .stButton>button {{
        border-radius: 50%;
        width: 50px;
        height: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

# عرض العنوان الضخم
st.markdown('<p class="revo-title">REVO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["user"] == "أحمد" else "other-bubble"
    st.markdown(f'<div class="{bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
    if "file" in msg:
        st.audio(msg["file"])

# --- 4. منطقة الإدخال (الزائد والأوديو حدا بعضياتهم) ---
st.write("---")
# تقسيم العرض لـ 3 بلايص: الزائد، الميكروفون، وخانة الكتابة
cols = st.columns([0.6, 0.6, 8])

with cols[0]:
    if st.button("➕", key="plus"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

with cols[1]:
    # زر الميكروفون لاصق مع الزائد
    audio_record = mic_recorder(start_prompt="🎤", stop_prompt="✅", key='recorder')

with cols[2]:
    prompt = st.chat_input("اكتب رسالة هنا...")
    if prompt:
        st.session_state.messages.append({"user": "أحمد", "text": prompt})
        st.rerun()

# معالجة تسجيل الأوديو
if audio_record:
    st.session_state.messages.append({
        "user": "أحمد", 
        "text": "🎙️ رسالة صوتية", 
        "file": audio_record['bytes']
    })
    st.rerun()

# منيو الزائد (إيلا تبرك عليها)
if st.session_state.get('show_menu', False):
    with st.expander("📎 إضافة وسائط", expanded=True):
        st.camera_input("📸 خذ صورة")
        st.file_uploader("📁 أرسل ملف")
