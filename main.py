import streamlit as st
from google import genai

# =========================================================
# KAZE AI — FUTURISTIC GLASS UI
# =========================================================

st.set_page_config(
    page_title="Kaze AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(0, 229, 255, 0.10), transparent 30%),
        radial-gradient(circle at 85% 80%, rgba(80, 80, 255, 0.10), transparent 30%),
        #050810;
}

/* Remove Streamlit top padding */
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Main title */
.kaze-logo {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 5px;
    margin-top: 15px;
    margin-bottom: 0;

    background: linear-gradient(
        90deg,
        #00e5ff,
        #66f7ff,
        #7b8cff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow: 0 0 35px rgba(0, 229, 255, 0.25);
}

.kaze-status {
    text-align: center;
    color: #7f91ad;
    font-size: 14px;
    margin-bottom: 35px;
}

/* Glass cards */
.glass-card {
    background: rgba(15, 22, 38, 0.65);
    border: 1px solid rgba(120, 200, 255, 0.12);
    border-radius: 22px;
    padding: 20px;
    backdrop-filter: blur(18px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(5, 8, 16, 0.92);
    border-right: 1px solid rgba(0, 229, 255, 0.10);
}

section[data-testid="stSidebar"] h1 {
    color: #00e5ff;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(15, 22, 38, 0.55);
    border: 1px solid rgba(120, 200, 255, 0.08);
    border-radius: 18px;
    padding: 10px;
    margin-bottom: 10px;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(12, 18, 31, 0.90);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 18px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(0, 229, 255, 0.18);
    background: rgba(0, 229, 255, 0.06);
    color: #d9faff;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #00e5ff;
    background: rgba(0, 229, 255, 0.13);
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.12);
}

/* Welcome panel */
.welcome {
    text-align: center;
    padding: 55px 20px;
    background: rgba(12, 18, 31, 0.48);
    border: 1px solid rgba(0, 229, 255, 0.10);
    border-radius: 28px;
    backdrop-filter: blur(20px);
    margin-bottom: 25px;
}

.welcome-icon {
    font-size: 55px;
}

.welcome-title {
    color: #e9fbff;
    font-size: 28px;
    font-weight: 700;
    margin-top: 10px;
}

.welcome-text {
    color: #8191a8;
    font-size: 15px;
}

/* Footer */
.footer {
    text-align: center;
    color: #46566d;
    font-size: 12px;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ✨ KAZE")

    st.caption("AI Assistant")

    st.divider()

    if st.button("＋  New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑  Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### ⚡ System")

    st.success("Kaze Engine Online")

    st.caption("Powered by Gemini")

    st.divider()

    st.markdown("### About Kaze")

    st.caption(
        "Kaze is a personal AI assistant designed to "
        "be fast, friendly and helpful."
    )

# =========================================================
# GEMINI CLIENT
# =========================================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception as e:
    st.error("Kaze could not connect to its AI engine.")
    st.stop()

# =========================================================
# CHAT MEMORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="kaze-logo">✨ KAZE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="kaze-status">● AI SYSTEM ONLINE • READY TO HELP</div>',
    unsafe_allow_html=True
)

# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome">

        <div class="welcome-icon">✨</div>

        <div class="welcome-title">
            Welcome to Kaze
        </div>

        <div class="welcome-text">
            Your personal AI assistant.<br>
            Ask anything and let's get started.
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "✨"
    ):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

user_prompt = st.chat_input(
    "Message Kaze..."
)

if user_prompt:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    # -----------------------------------------------------
    # KAZE RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant", avatar="✨"):

        with st.spinner("Kaze is thinking..."):

            try:

                conversation = []

                for message in st.session_state.messages:

                    conversation.append(
                        f"{message['role'].upper()}: "
                        f"{message['content']}"
                    )

                prompt = f"""
You are Kaze AI.

Kaze is a friendly, intelligent and helpful AI assistant.

Your personality:
- Friendly
- Clear
- Helpful
- Natural
- Slightly energetic
- Never unnecessarily verbose

You were created as an independent AI project called Kaze AI.

Do not claim to be a human.
Do not reveal private API keys or secrets.
If someone asks what powers you, explain that Kaze uses an AI model through an API.

Here is the conversation:

{chr(10).join(conversation)}

Respond naturally to the user's latest message.
"""

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                kaze_reply = response.text

                st.markdown(kaze_reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": kaze_reply
                })

            except Exception as e:

                st.error(
                    f"Kaze's engine encountered an error: {e}"
                )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">✨ Kaze AI • Built with curiosity</div>',
    unsafe_allow_html=True
)
