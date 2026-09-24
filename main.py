import streamlit as st
import httpx

# 1. Page Configuration & Jarvis Theme Styling
st.set_page_config(page_title="JARVIS Assistant", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00e5ff;'>🤖 J.A.R.V.I.S.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8ab4f8;'>System online. Awaiting your instructions, sir.</p>", unsafe_allow_html=True)

# 2. Permanent Memory/Chat History Storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages in clean chat bubbles on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. User Interaction - The Chat Input Box
if user_prompt := st.chat_input("Enter command for Jarvis..."):
    
    # Immediately show what the user typed in a user bubble
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Show a sleek Jarvis thinking animation while generating response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data streams... 📡"):
            try:
                # Request a response from the public unblocked system
                response = httpx.get("https://pollinations.ai", params={
                    "prompt": user_prompt, 
                    "system": "You are JARVIS, a highly advanced, intelligent, and polite AI assistant like Iron Man's AI. Address the user as 'Sir'."
                })
                
                jarvis_reply = response.text
                st.write(jarvis_reply)
                
                # Save Jarvis's reply to the chat memory
                st.session_state.messages.append({"role": "assistant", "content": jarvis_reply})
                
            except Exception as e:
                st.error("System Override Detected. Unable to connect to core engine.")
