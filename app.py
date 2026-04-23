import streamlit as st
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة
st.set_page_config(page_title="REVO 💬", page_icon="💬", layout="centered")

# --- 2. إضافة اختيار الألوان في الجنب ---
with st.sidebar:
    st.markdown("### 🎨 تخصيص المظهر")
    # هاد الألوان هما اللي صيفطتي لي في الصور
    theme_choice = st.selectbox(
        "اختار لون الخلفية:",
        ["الأخضر الهادئ", "الأزرق السماوي", "الوردي الناعم", "الأصفر المشرق", "الذهبي"]
    )
    
    # ربط الاختيار بالكود ديال الألوان (Gradients)
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

# --- 3. CSS الديناميكي (كيتغير حسب الاختيار) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_gradient};
    }}
    .revo-title {{
        font-family: 'Courier New', Courier, monospace;
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #128C7E;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    .chat-bubble {{
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }}
    .user-bubble {{ background-color: #DCF8C6; margin-left: auto; border-bottom-right-radius: 2px; }}
    .other-bubble {{ background-color: #FFFFFF; margin-right: auto; border-bottom-left-radius: 2px; border: 1px solid #E5E5E5; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="revo-title">💬 ℛℰ𝒱𝒪 💬</p>', unsafe_allow_html=True)

# باقي الكود (المحادثة والوسائط) كيبقى هو هو...
if "messages" not in st.session_state:
    st.session_state.messages = []

user_name = st.sidebar.text_input("سميتك:", value="أحمد")

# عرض الرسائل
for msg in st.session_state.messages:
    is_me = msg["user"] == user_name
    bubble_class = "user-bubble" if is_me else "other-bubble"
    st.markdown(f'<div class="chat-bubble {bubble_class}"><b>{msg["user"]}</b><br>{msg["text"]}</div>', unsafe_allow_html=True)

# شريط الإدخال السفلي
cols = st.columns([1, 10])
with cols[0]:
    if st.button("➕"):
        st.session_state.show_menu = not st.session_state.get('show_menu', False)

if st.session_state.get('show_menu', False):
    with st.expander("📎 الوسائط", expanded=True):
        # (نفس كود الميديا اللي درنا قبل)
        pass

with cols[1]:
    if prompt := st.chat_input("اكتب رسالة..."):
        st.session_state.messages.append({"user": user_name, "text": prompt})
        st.rerun()
