import streamlit as st
from google import genai

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Kaze",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# GEMINI
# -----------------------------
api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -20%, #202020 0%, #0b0b0d 42%, #050506 100%);
    color: #f5f5f5;
}

/* Remove Streamlit top padding */
.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 8rem;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* -----------------------------
   TOP BAR
----------------------------- */

.kaze-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 4px 20px 4px;
}

.kaze-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.kaze-logo {
    width: 30px;
    height: 30px;
    border-radius: 10px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(135deg, #ffffff, #8d8d8d);
    color: #050505;

    font-size: 14px;
    font-weight: 800;

    box-shadow: 0 0 25px rgba(255,255,255,0.08);
}

.kaze-name {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.4px;
}

.kaze-version {
    color: #777;
    font-size: 11px;
    margin-left: 5px;
}

/* -----------------------------
   WELCOME
----------------------------- */

.welcome {
    min-height: 55vh;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    text-align: center;
    padding-top: 30px;
}

.welcome-small {
    color: #8b8b8b;
    font-size: 13px;
    margin-bottom: 12px;
}

.welcome-title {
    font-size: clamp(38px, 6vw, 64px);
    font-weight: 600;
    letter-spacing: -3px;
    line-height: 1.05;

    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #bdbdbd 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 14px;
}

.welcome-subtitle {
    color: #777;
    font-size: 15px;
}

/* -----------------------------
   SUGGESTIONS
----------------------------- */

.suggestions {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;

    margin-top: 38px;
    width: 100%;
    max-width: 850px;
}

.suggestion {
    padding: 17px;
    min-height: 80px;

    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 17px;

    background: rgba(255,255,255,0.025);

    text-align: left;

    transition: 0.2s ease;
}

.suggestion:hover {
    background: rgba(255,255,255,0.055);
    border-color: rgba(255,255,255,0.13);
    transform: translateY(-2px);
}

.suggestion-icon {
    font-size: 16px;
    margin-bottom: 9px;
}

.suggestion-title {
    font-size: 13px;
    color: #ddd;
    font-weight: 500;
}

.suggestion-text {
    color: #666;
    font-size: 11px;
    margin-top: 4px;
}

/* -----------------------------
   CHAT MESSAGES
----------------------------- */

.chat-wrapper {
    max-width: 850px;
    margin: 25px auto;
}

.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 18px 0;
}

.user-bubble {
    max-width: 75%;

    padding: 12px 16px;

    border-radius: 18px 18px 5px 18px;

    background: #eeeeee;
    color: #111;

    font-size: 14px;
    line-height: 1.55;
}

.ai-message {
    display: flex;
    gap: 12px;
    margin: 22px 0;
}

.ai-avatar {
    width: 27px;
    height: 27px;

    min-width: 27px;

    border-radius: 9px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #eeeeee;
    color: #111;

    font-size: 11px;
    font-weight: 700;
}

.ai-content {
    color: #d5d5d5;
    font-size: 14px;
    line-height: 1.7;

    max-width: 80%;
}

/* -----------------------------
   INPUT
----------------------------- */

.stChatInput {
    padding-bottom: 20px !important;
}

.stChatInput > div {
    background: rgba(18,18,20,0.92) !important;

    border: 1px solid rgba(255,255,255,0.09) !important;

    border-radius: 20px !important;

    box-shadow:
        0 10px 40px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.03);
}

.stChatInput textarea {
    color: #f5f5f5 !important;
}

.stChatInput textarea::placeholder {
    color: #666 !important;
}

/* -----------------------------
   BUTTONS
----------------------------- */

div.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);

    background: rgba(255,255,255,0.035);

    color: #ddd;

    transition: 0.2s ease;
}

div.stButton > button:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.15);
}

/* -----------------------------
   SIDEBAR
----------------------------- */

section[data-testid="stSidebar"] {
    background: #080809;
    border-right: 1px solid rgba(255,255,255,0.06);
}

.sidebar-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
}

.sidebar-text {
    color: #666;
    font-size: 12px;
    line-height: 1.6;
}

/* -----------------------------
   MOBILE
----------------------------- */

@media (max-width: 700px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .welcome-title {
        font-size: 42px;
        letter-spacing: -2px;
    }

    .suggestions {
        grid-template-columns: repeat(2, 1fr);
    }

    .user-bubble {
        max-width: 88%;
    }

    .ai-content {
        max-width: 88%;
    }
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TOP BAR
# -----------------------------

st.markdown("""
<div class="kaze-topbar">

    <div class="kaze-brand">
        <div class="kaze-logo">K</div>
        <div class="kaze-name">
            Kaze
            <span class="kaze-version">AI</span>
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Kaze</div>',
        unsafe_allow_html=True
    )

    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="sidebar-text">
        Your conversations stay inside this session.
        <br><br>
        Powered by Gemini.
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# WELCOME SCREEN
# -----------------------------

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome">

        <div class="welcome-small">
            Welcome to Kaze
        </div>

        <div class="welcome-title">
            What can I help with?
        </div>

        <div class="welcome-subtitle">
            Ask anything. Build something. Learn something.
        </div>

        <div class="suggestions">

            <div class="suggestion">
                <div class="suggestion-icon">✦</div>
                <div class="suggestion-title">Ideas</div>
                <div class="suggestion-text">Brainstorm something new</div>
            </div>

            <div class="suggestion">
                <div class="suggestion-icon">⌘</div>
                <div class="suggestion-title">Code</div>
                <div class="suggestion-text">Build and debug projects</div>
            </div>

            <div class="suggestion">
                <div class="suggestion-icon">◌</div>
                <div class="suggestion-title">Learn</div>
                <div class="suggestion-text">Understand difficult topics</div>
            </div>

            <div class="suggestion">
                <div class="suggestion-icon">↗</div>
                <div class="suggestion-title">Create</div>
                <div class="suggestion-text">Turn ideas into reality</div>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <div class="user-bubble">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-message">

                <div class="ai-avatar">
                    K
                </div>

                <div class="ai-content">
                    {message["content"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# CHAT INPUT
# -----------------------------

prompt = st.chat_input("Ask Kaze anything...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Build conversation for Gemini
    conversation = []

    for message in st.session_state.messages:

        conversation.append(
            f"{message['role'].upper()}: {message['content']}"
        )

    full_prompt = "\n\n".join(conversation)

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt
        )

        answer = response.text

    except Exception as e:

        answer = f"Sorry, something went wrong:\n\n`{e}`"

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
