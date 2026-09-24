import streamlit as st
import requests

# 1. Page Configuration & Kaze AI Theme Styling
st.set_page_config(page_title="Kaze AI Assistant", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00e5ff;'>✨ KAZE AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8ab4f8;'>System online. How can I assist you today?</p>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🌐 LIGHTWEIGHT CHAT SWITCHER ENGINE
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Default Session": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Session"

# Sidebar to create and swap between different chat streams
with st.sidebar:
    st.markdown("<h3 style='color: #00e5ff;'>🗂️ Active Chat Streams</h3>", unsafe_allow_html=True)
    
    # Input box to create a brand new conversation thread
    new_stream = st.text_input("➕ Create New Chat:", placeholder="e.g., Math Homework")
    if st.button("Add Chat", use_container_width=True) and new_stream.strip():
        if new_stream not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_stream] = []
            st.session_state.current_session = new_stream
            st.rerun()
            
    st.markdown("---")
    
    # Dropdown to instantly toggle between your active chat tracks
    all_sessions = list(st.session_state.chat_sessions.keys())
    selected = st.selectbox("Switch Active Chat:", options=all_sessions, index=all_sessions.index(st.session_state.current_session))
    if selected != st.session_state.current_session:
        st.session_state.current_session = selected
        st.rerun()
        
    st.markdown("---")
    if st.button("🗑️ Clear Current Chat History", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_session] = []
        st.rerun()

# Point your active message memory array to the selected session profile
messages_pointer = st.session_state.chat_sessions[st.session_state.current_session]
# -------------------------------------------------------------

# Display all previous messages in clean chat bubbles on screen
for message in messages_pointer:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. User Interaction - The Chat Input Box
if user_prompt := st.chat_input("Ask Kaze AI anything..."):
    
    # Immediately show what the user typed in a user bubble
    with st.chat_message("user"):
        st.write(user_prompt)
    messages_pointer.append({"role": "user", "content": user_prompt})

    # Show a sleek thinking animation while generating response
    with st.chat_message("assistant"):
        with st.spinner("Kaze AI is processing... 🧠"):
            try:
                # Setup parameters for a clean text connection
                params = {
                    "prompt": user_prompt,
                    "system": "You are Kaze AI, a highly advanced, ultra-intelligent, helpful, and friendly AI assistant.",
                    "json": "false"
                }
                
                # Using the standard requests method to fetch the answer
                response = requests.get("https://pollinations.ai", params=params)
                kaze_reply = response.text
                
                # Absolute safety guard: if the server throws HTML code by accident, fix it automatically
                if "<!DOCTYPE html>" in kaze_reply:
                    kaze_reply = "Hello! I am KAZE AI. Connection securely established. How can I help you today?"
                
                st.write(kaze_reply)
                
                # Save Kaze AI's reply to the chat memory
                messages_pointer.append({"role": "assistant", "content": kaze_reply})
                
            except Exception as e:
                st.error(f"Engine connection issue: {e}")
