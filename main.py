import streamlit as st
import requests

# 1. Page Configuration & Kaze AI Theme Styling
st.set_page_config(page_title="Kaze AI Assistant", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00e5ff;'>✨ KAZE AI V2</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8ab4f8;'>System fully upgraded. I can chat, solve problems, and generate IMAGES!</p>", unsafe_allow_html=True)

# 2. Permanent Memory/Chat History Storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎛️ SIDEBAR MENU: Clear Chat Button
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.write("Manage your AI application features:")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("💡 **Tip:** Type the word **'image'** in your prompt to make the AI draw something!")

# Display all previous messages in clean chat bubbles on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.write(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message["caption"])

# 3. User Interaction - The Chat Input Box
if user_prompt := st.chat_input("Ask Kaze AI anything or generate an image..."):
    
    # Immediately show what the user typed in a user bubble
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt, "type": "text"})

    # Check if the user is asking for an image
    if "image" in user_prompt.lower() or "draw" in user_prompt.lower() or "picture" in user_prompt.lower():
        with st.chat_message("assistant"):
            with st.spinner("🎨 Kaze AI is painting your masterpiece..."):
                try:
                    # Direct API connection to Pollinations image engine
                    image_url = f"https://pollinations.ai{requests.utils.quote(user_prompt)}?width=1024&height=1024&nologo=true"
                    
                    st.image(image_url, caption=f"Generated: '{user_prompt}'")
                    st.session_state.messages.append({"role": "assistant", "content": image_url, "type": "image", "caption": user_prompt})
                except Exception as e:
                    st.error(f"Image generation failed: {e}")
    else:
        # Standard Text Chat Mode
        with st.chat_message("assistant"):
            with st.spinner("Kaze AI is processing... 🧠"):
                try:
                    params = {
                        "system": "You are Kaze AI, a highly advanced, ultra-intelligent, helpful, and friendly AI assistant.",
                        "json": "false"
                    }
                    response = requests.get(f"https://pollinations.ai{user_prompt}", params=params)
                    kaze_reply = response.text
                    
                    st.write(kaze_reply)
                    st.session_state.messages.append({"role": "assistant", "content": kaze_reply, "type": "text"})
                    
                except Exception as e:
                    st.error(f"Engine connection issue: {e}")
