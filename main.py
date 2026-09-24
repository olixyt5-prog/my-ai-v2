import streamlit as st
import requests

# 1. Premium Dark Blue & Cyan Sci-Fi Glassmorphism Interface Design
st.set_page_config(page_title="KAZE AI QUANTUM", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* Premium Overall Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #020c1b 0%, #0d1b2a 100%);
        color: #e0e1dd;
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean Sidebar Custom Makeover */
    section[data-testid="stSidebar"] {
        background-color: #030814 !important;
        border-right: 2px solid #00b4d8;
    }
    
    /* User Chat Bubble Accent Styling */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background: rgba(0, 180, 216, 0.15) !important;
        border: 1px solid #00b4d8 !important;
        border-radius: 15px 15px 0px 15px !important;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    /* Assistant Chat Bubble Accent Styling */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {
        background: rgba(13, 27, 42, 0.8) !important;
        border: 1px solid #0077b6 !important;
        border-radius: 15px 15px 15px 0px !important;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    /* Sleek Title Header Font Layout */
    .quantum-title {
        text-align: center;
        background: linear-gradient(90deg, #00f5ff, #0077b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        letter-spacing: 2px;
        margin-bottom: 5px;
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
    st.markdown("<h2 style='color: #00b4d8; font-weight: 700;'>⚙️ CORE SYSTEMS</h2>", unsafe_allow_html=True)
    st.write("Manage active neural data streams:")
    
    # Input to add a brand new chat stream
    new_chat_name = st.text_input("➕ Create New Chat Stream:", placeholder="e.g., Homework Helper")
    if st.button("Initialize Stream", use_container_width=True) and new_chat_name.strip():
        if new_chat_name not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_chat_name] = []
            st.session_state.current_session = new_chat_name
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='color: #0077b6; font-weight: bold;'>🗂️ ACTIVE CHAT STREAMS</p>", unsafe_allow_html=True)
    
    # Dropdown to swap between chat streams
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
    st.write("💡 *Tip: Type 'image' anywhere in your prompt to activate the paint engine module.*")

# Grab active history list based on what session is active
current_history = st.session_state.chat_sessions[st.session_state.current_session]

# 4. Premium Visual Layout Headers
st.markdown("<div class='quantum-title'>⚡ KAZE AI QUANTUM</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #8ecae6;'>Stream: <span style='color: #00f5ff;'><b>{st.session_state.current_session}</b></span> | Engine Connection: Secured</p>", unsafe_allow_html=True)
st.markdown("---")

# Display previous messages in design context
for message in current_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.write(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message["caption"])

# 5. User Input Threat Engine
if user_prompt := st.chat_input("Send a instruction payload to Kaze AI..."):
    
    # Instantly output user bubble
    with st.chat_message("user"):
        st.write(user_prompt)
    current_history.append({"role": "user", "content": user_prompt, "type": "text"})

    # Check if asking for an image
    if any(keyword in user_prompt.lower() for keyword in ["image", "draw", "picture", "paint"]):
        with st.chat_message("assistant"):
            with st.spinner("🎨 Reconfiguring neural nodes for artistic generation..."):
                try:
                    encoded_prompt = requests.utils.quote(user_prompt)
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    st.image(image_url, caption=f"Compiled Artifact: '{user_prompt}'")
                    current_history.append({"role": "assistant", "content": image_url, "type": "image", "caption": user_prompt})
                except Exception as e:
                    st.error(f"Art generation fault: {e}")
    else:
        # Standard Clean Text Stream Path
        with st.chat_message("assistant"):
            with st.spinner("Decoding digital frequencies... 🌐"):
                try:
                    encoded_text = requests.utils.quote(user_prompt)
                    # Forcing a precise text-only endpoint format
                    system_prompt = requests.utils.quote("You are Kaze AI Quantum, a brilliant cybernetic chatbot assistant wrapped in a sleek blue visual layout.")
                    
                    api_url = f"https://pollinations.ai{encoded_text}?system={system_prompt}"
                    
                    response = requests.get(api_url)
                    kaze_reply = response.text
                    
                    st.write(kaze_reply)
                    current_history.append({"role": "assistant", "content": kaze_reply, "type": "text"})
                except Exception as e:
                    st.error(f"Neural core feedback fault: {e}")
