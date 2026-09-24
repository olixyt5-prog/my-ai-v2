import streamlit as st
import requests

# 1. Custom Premium Dark Blue Theme Styling
st.set_page_config(page_title="Kaze AI Quantum Console", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* Main Background & Text Color Styling */
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    /* Sleek User Chat Bubble Accent */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background-color: #1b263b !important;
        border-left: 5px solid #00b4d8 !important;
        border-radius: 10px;
    }
    /* Sleek Assistant Chat Bubble Accent */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {
        background-color: #415a77 !important;
        border-left: 5px solid #0077b6 !important;
        border-radius: 10px;
    }
    /* Custom Sidebar Styling Overrides */
    section[data-testid="stSidebar"] {
        background-color: #0b132b !important;
        border-right: 1px solid #1c2541;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Setup Multiple Chats Session Engine
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Default Session": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Session"

# 3. 🎛️ SIDEBAR CONTROL PANEL: Multiple Chats System
with st.sidebar:
    st.markdown("<h2 style='color: #00b4d8;'>⚙️ Core Systems</h2>", unsafe_allow_html=True)
    st.write("Manage active neural data streams:")
    
    # Text input box to add a brand new chat session name
    new_chat_name = st.text_input("➕ Create New Chat Stream:", placeholder="e.g., Science Project")
    if st.button("Initialize Stream", use_container_width=True) and new_chat_name.strip():
        if new_chat_name not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_chat_name] = []
            st.session_state.current_session = new_chat_name
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='color: #0077b6; font-weight: bold;'>🗂️ Active Chat Streams</p>", unsafe_allow_html=True)
    
    # Dropdown selector to instantly swap between different active chat histories
    session_list = list(st.session_state.chat_sessions.keys())
    selected_session = st.selectbox(
        "Select Active Neural Stream:", 
        options=session_list, 
        index=session_list.index(st.session_state.current_session)
    )
    if selected_session != st.session_state.current_session:
        st.session_state.current_session = selected_session
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Purge Current History", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_session] = []
        st.rerun()
    st.write("💡 *Type 'image' or 'draw' to swap the engine directly into painting mode.*")

# Grab the active chat history list based on what session is currently active
current_history = st.session_state.chat_sessions[st.session_state.current_session]

# 4. Premium Visual Layout Headers
st.markdown("<h1 style='text-align: center; color: #00b4d8;'>⚡ KAZE AI QUANTUM</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #8ecae6;'>Active Stream: <b>{st.session_state.current_session}</b> | Engine Status: Online</p>", unsafe_allow_html=True)

# Loop and display all previous chat elements cleanly in historical context
for message in current_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.write(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message["caption"])

# 5. Active User Input Thread Engine
if user_prompt := st.chat_input("Inject payload instruction to console..."):
    
    # Instantly output the user statement
    with st.chat_message("user"):
        st.write(user_prompt)
    current_history.append({"role": "user", "content": user_prompt, "type": "text"})

    # AI Decision Matrix: Image Mode Check
    if any(keyword in user_prompt.lower() for keyword in ["image", "draw", "picture", "paint"]):
        with st.chat_message("assistant"):
            with st.spinner("🎨 Reconfiguring subsystem matrix for artistic compilation..."):
                try:
                    # Clean encoding for image strings
                    encoded_prompt = requests.utils.quote(user_prompt)
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    st.image(image_url, caption=f"Compiled Artifact: '{user_prompt}'")
                    current_history.append({"role": "assistant", "content": image_url, "type": "image", "caption": user_prompt})
                except Exception as e:
                    st.error(f"Art module matrix compile error: {e}")
    else:
        # Standard NLP Conversation Core Processing
        with st.chat_message("assistant"):
            with st.spinner("Compiling tactical solution array... 🌐"):
                try:
                    # Explicit separation query variables to stop domain smashing loops
                    params = {
                        "text": user_prompt,
                        "system": "You are Kaze AI Quantum, a state-of-the-art supercomputer assistant running on a dark blue cybernetic terminal layout.",
                        "json": "false"
                    }
                    # Pointed to a clean parameters pathway target
                    response = requests.get("https://pollinations.ai", params=params)
                    kaze_reply = response.text
                    
                    st.write(kaze_reply)
                    current_history.append({"role": "assistant", "content": kaze_reply, "type": "text"})
                except Exception as e:
                    st.error(f"Neural core feedback exception: {e}")
