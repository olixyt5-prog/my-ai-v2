import streamlit as st
import google.generativeai as genai

# 1. Page Configuration & Gemini Styling Layout
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="✨", layout="centered")

st.title("✨ My Custom Gemini AI")
st.write("Ask anything, explore ideas, or just chat with my new brain!")

# 2. THE ULTIMATE BYPASS KEY
# PASTE YOUR NEW ALZaSy... KEY INSIDE THESE QUOTES DIRECTLY:
API_KEY = "AQ.Ab8RN6Im9omIPuqx4W9L804kc76pXRjUcjBKWk-2_7QJEzvdA"
# Configure the core engine
genai.configure(api_key=API_KEY)

# 3. Create a Permanent Memory/Chat History Storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages in clean chat bubbles on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. User Interaction - The Bottom Chat Input Box
if user_prompt := st.chat_input("Ask Gemini anything..."):
    
    # Immediately show what the user typed in a user bubble
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Show a sleek thinking animation while generating response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                # Call the completely stable chat engine model
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_prompt)
                
                ai_reply = response.text
                st.write(ai_reply)
                
                # Save the AI's reply to the chat memory
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except Exception as e:
                st.error(f"Error connecting to AI engine: {e}")
