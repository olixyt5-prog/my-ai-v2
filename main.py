import streamlit as st
from google import genai

# -----------------------------
# KAZE AI - CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Kaze AI",
    page_icon="✨",
    layout="centered"
)

# -----------------------------
# KAZE AI THEME
# -----------------------------
st.markdown("""
<style>
.kaze-title {
    text-align: center;
    color: #00e5ff;
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 0;
}

.kaze-subtitle {
    text-align: center;
    color: #8ab4f8;
    font-size: 16px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="kaze-title">✨ KAZE AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="kaze-subtitle">Your AI assistant. Fast, helpful, and always ready.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# GEMINI CONNECTION
# -----------------------------
try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception:
    st.error("Kaze could not connect to its AI engine.")
    st.stop()

# -----------------------------
# CHAT MEMORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
user_prompt = st.chat_input("Ask Kaze AI anything...")

if user_prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    # Generate Kaze response
    with st.chat_message("assistant"):
        with st.spinner("Kaze is thinking... 🧠"):

            try:
                # Build conversation history
                conversation = []

                for message in st.session_state.messages:
                    conversation.append(
                        f"{message['role'].upper()}: {message['content']}"
                    )

                prompt = f"""
You are Kaze AI, a friendly, intelligent and helpful AI assistant.

You were created as a personal AI project called Kaze AI.

Be helpful, clear, and friendly.
Do not mention that you are Gemini unless the user specifically asks what AI model powers you.

Conversation:

{chr(10).join(conversation)}

KAZE:
"""

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                kaze_reply = response.text

                st.markdown(kaze_reply)

                # Save response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": kaze_reply
                })

            except Exception as e:
                st.error(f"Kaze's engine encountered an error: {e}")
