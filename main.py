import streamlit as st
import requests

# 1. High-Performance Blue Interface Layout
st.set_page_config(page_title="KAZE AI", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    /* Background and Global Styles */
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    /* Simple User Chat Box */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background-color: #1b263b !important;
        border-radius: 10px;
    }
    /* Simple Assistant Chat Box */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {
        background-color: #0b132b !important;
        border-radius: 10px;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #030814 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Optimized Multi-Chat Memory Storage
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Default Session": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Session"

# 3. Sidebar Panel
with st.sidebar:
    st.markdown("<h3 style='color: #00b4d8;'>⚙️ KAZE AI CORE</h3>", unsafe_allow_html=True)
    
    # Session Creator
    new_chat_name = st.text_input("➕ New Chat Stream:", placeholder="Name your new chat...")
    if st.button("Create Stream", use_container_width=True) and new_chat_name.strip():
        if new_chat_name not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_chat_name] = []
            st.session_state.current_session = new_chat_name
            st.rerun()

    st.markdown("---")
    
    # Active Streams List
    session_list = list(st.session_state.chat_sessions.keys())
    selected_session = st.selectbox("Active Stream:", options=session_list, index=session_list.index(st.session_state.current_session))
    if selected_session != st.session_state.current_session:
        st.session_state.current_session = selected_session
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear This Chat", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_session] = []
        st.rerun()

# Reference for the active conversation history thread
current_history = st.session_state.chat_sessions[st.session_state.current_session]

# 4. Premium Headings
st.markdown("<h1 style='text-align: center; color: #00b4d8; font-weight:800;'>⚡ KAZE AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #8ecae6;'>Active Stream: <b>{st.session_state.current_session}</b></p>", unsafe_allow_html=True)
st.markdown("---")

# Render active log
for message in current_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.write(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message["caption"])

# 5. Core Operational Input Form Box
if user_prompt := st.chat_input("Message KAZE AI..."):
    with st.chat_message("user"):
        st.write(user_prompt)
    current_history.append({"role": "user", "content": user_prompt, "type": "text"})

    # Check for Image Generation Keywords
    if any(kw in user_prompt.lower() for kw in ["image", "draw", "picture", "paint"]):
        with st.chat_message("assistant"):
            with st.spinner("🎨 Generating image..."):
                try:
                    encoded_prompt = requests.utils.quote(user_prompt)
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    st.image(image_url, caption=f"Generated Image: '{user_prompt}'")
                    current_history.append({"role": "assistant", "content": image_url, "type": "image", "caption": user_prompt})
                except Exception as e:
                    st.error(f"Art Engine Fault: {e}")
    else:
        # Standard Fast Text Process
        with st.chat_message("assistant"):
            with st.spinner("Processing... 🌐"):
                try:
                    api_url = "https://pollinations.ai"
                    payload = {
                        "prompt": user_prompt,
                        "system": "You are KAZE AI, a helpful, brilliant, and friendly AI assistant wrapped in a sleek blue dashboard theme.",
                        "json": "false"
                    }
                    response = requests.get(api_url, params=payload)
                    kaze_reply = response.text
                    
                    st.write(kaze_reply)
                    current_history.append({"role": "assistant", "content": kaze_reply, "type": "text"})
                except Exception as e:
                    st.error(f"Connection Fault: {e}")
