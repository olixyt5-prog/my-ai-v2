import streamlit as st
import requests

# 1. Page Configuration & Kaze AI Theme Styling
st.set_page_config(page_title="Kaze AI Assistant", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00e5ff;'>✨ KAZE AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8ab4f8;'>System online. How can I assist you today?</p>", unsafe_allow_html=True)

# 2. Permanent Memory/Chat History Storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages in clean chat bubbles on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. User Interaction - The Chat Input Box
if user_prompt := st.chat_input("Ask Kaze AI anything..."):
    
    # Immediately show what the user typed in a user bubble
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Show a sleek thinking animation while generating response
    with st.chat_message("assistant"):
        with st.spinner("Kaze AI is processing... 🧠"):
            try:
                # Setup parameters for a clean text connection
                params = {
                    "system": "You are Kaze AI, a highly advanced, ultra-intelligent, helpful, and friendly AI assistant.",
                    "json": "false"
                }
                
                # Using the standard requests method to fetch the answer
                response = requests.get(f"https://text.pollinations.ai/{user_prompt}", params=params)
                kaze_reply = response.text
                
                st.write(kaze_reply)
                
                # Save Kaze AI's reply to the chat memory
                st.session_state.messages.append({"role": "assistant", "content": kaze_reply})
                
            except Exception as e:
                st.error(f"Engine connection issue: {e}")
