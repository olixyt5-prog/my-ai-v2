import streamlit as st
import requests

# 1. Clean Pro Midnight-Blue Layout
st.set_page_config(page_title="KAZE AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    section[data-testid="stSidebar"] { background-color: #030712 !important; border-right: 1px solid #1f2937; }
    div[data-testid="stChatMessage"] { border-radius: 12px !important; margin-bottom: 12px; padding: 14px; }
    </style>
""", unsafe_allow_html=True)

# 2. Multiple Chats Engine
if "chats" not in st.session_state:
    st.session_state.chats = {"Default Session": []}
if "active" not in st.session_state:
    st.session_state.active = "Default Session"

# 3. Sidebar Navigation Panel
with st.sidebar:
    st.markdown("<h3 style='color: #ffffff;'>⚡ KAZE AI INTERFACE</h3>", unsafe_allow_html=True)
    new_name = st.text_input("➕ New Chat Session Name:")
    if st.button("Create Session", use_container_width=True) and new_name.strip():
        if new_name not in st.session_state.chats:
            st.session_state.chats[new_name] = []
            st.session_state.active = new_name
            st.rerun()
    
    st.markdown("---")
    sessions = list(st.session_state.chats.keys())
    chosen = st.selectbox("Switch Active Session:", options=sessions, index=sessions.index(st.session_state.active))
    if chosen != st.session_state.active:
        st.session_state.active = chosen
        st.rerun()

history = st.session_state.chats[st.session_state.active]

# 4. Main Title Header Layout
st.markdown("<h1 style='text-align: center; color: #ffffff; font-weight:800;'>KAZE AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #9ca3af;'>Active Session: <b>{st.session_state.active}</b></p>", unsafe_allow_html=True)
st.markdown("---")

# Render active conversation log lines cleanly
for msg in history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text": st.write(msg["content"])
        else: st.image(msg["content"])

# 5. Core Operational Form Input Field Block
if user_prompt := st.chat_input("Message KAZE AI..."):
    with st.chat_message("user"):
        st.write(user_prompt)
    history.append({"role": "user", "content": user_prompt, "type": "text"})

    # Check for Image Generation Keywords
    if any(kw in user_prompt.lower() for kw in ["image", "draw", "picture", "paint"]):
        with st.chat_message("assistant"):
            with st.spinner("🎨 Generating image..."):
                try:
                    url = f"https://pollinations.ai{requests.utils.quote(user_prompt)}?width=1024&height=1024&nologo=true"
                    st.image(url)
                    history.append({"role": "assistant", "content": url, "type": "image"})
                except Exception as e:
                    st.error(f"Art Module Fault: {e}")
    else:
        # Standard Fast Text Process
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Bulletproof parameter separation endpoint to prevent page code dumping loops
                    response = requests.get("https://pollinations.ai", params={
                        "prompt": user_prompt,
                        "system": "You are KAZE AI, a brilliant, professional, and friendly AI chatbot helper.",
                        "json": "false"
                    })
                    reply = response.text
                    st.write(reply)
                    history.append({"role": "assistant", "content": reply, "type": "text"})
                except Exception as e:
                    st.error(f"Connection Fault: {e}")
