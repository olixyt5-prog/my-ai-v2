import streamlit as st
import time
from google import genai

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Kaze AI",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GEMINI
# =========================================================

api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"

# =========================================================
# SESSION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# SIMPLE CLEAN CSS
# =========================================================

st.markdown("""
<style>

/* -----------------------------
   PAGE
----------------------------- */

.stApp {
    background: #ffffff;
    color: #202123;
}

/* -----------------------------
   MAIN CONTENT
----------------------------- */

.block-container {
    max-width: 900px;
    padding-top: 1rem;
    padding-bottom: 120px;
}

/* -----------------------------
   HEADER
----------------------------- */

.kaze-header {
    display: flex;
    align-items: center;
    gap: 10px;

    padding: 10px 0 18px;

    border-bottom: 1px solid #eeeeee;

    margin-bottom: 20px;
}

.kaze-logo {
    width: 32px;
    height: 32px;

    border-radius: 8px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #111111;
    color: white;

    font-weight: 700;
    font-size: 15px;
}

.kaze-name {
    font-size: 18px;
    font-weight: 600;
    color: #202123;
}

.kaze-subtitle {
    font-size: 12px;
    color: #8e8e8e;
    margin-left: 3px;
}

/* -----------------------------
   WELCOME
----------------------------- */

.welcome {
    text-align: center;
    padding: 150px 20px 80px;
}

.welcome h1 {
    font-size: 32px;
    font-weight: 600;
    color: #202123;
    margin-bottom: 10px;
}

.welcome p {
    color: #777777;
    font-size: 15px;
}

/* -----------------------------
   CHAT
----------------------------- */

[data-testid="stChatMessage"] {
    padding: 15px 5px !important;
    background: transparent !important;
    border: none !important;
}

/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #f7f7f8 !important;

    border-radius: 12px !important;

    margin: 5px 0;
}

/* Assistant message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: white !important;

    margin: 5px 0;
}

/* Text */

[data-testid="stChatMessage"] p {
    font-size: 15px;
    line-height: 1.65;
}

/* -----------------------------
   INPUT
----------------------------- */

[data-testid="stChatInput"] {
    padding-bottom: 20px;
}

[data-testid="stChatInput"] > div {
    border: 1px solid #d9d9d9 !important;

    border-radius: 14px !important;

    background: white !important;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.05) !important;
}

[data-testid="stChatInput"] textarea {
    color: #202123 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #999999 !important;
}

/* -----------------------------
   SIDEBAR
----------------------------- */

section[data-testid="stSidebar"] {
    background: #f7f7f8;

    border-right: 1px solid #e5e5e5;
}

.sidebar-title {
    font-size: 18px;
    font-weight: 600;

    margin-bottom: 20px;
}

.sidebar-info {
    color: #777777;
    font-size: 12px;
    line-height: 1.6;

    margin-top: 25px;
}

/* Buttons */

.stButton > button {
    border-radius: 8px;

    border: 1px solid #dddddd;

    background: white;

    color: #333333;
}

.stButton > button:hover {
    background: #eeeeee;
}

/* -----------------------------
   MOBILE
----------------------------- */

@media (max-width: 700px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .welcome {
        padding-top: 120px;
    }

    .welcome h1 {
        font-size: 28px;
    }

}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="kaze-header">

    <div class="kaze-logo">
        K
    </div>

    <div class="kaze-name">
        Kaze
        <span class="kaze-subtitle">AI</span>
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Kaze</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋ New chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    if st.button(
        "Clear chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="sidebar-info">
        Kaze is your AI assistant for
        questions, coding, learning,
        brainstorming and more.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">

        <h1>How can I help you?</h1>

        <p>
            Ask Kaze anything.
        </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================================================
# INPUT
# =========================================================

prompt = st.chat_input(
    "Message Kaze..."
)

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================================
    # CONVERSATION
    # =====================================================

    conversation = []

    for message in st.session_state.messages:

        role = message["role"].upper()

        conversation.append(
            f"{role}: {message['content']}"
        )

    full_prompt = "\n\n".join(conversation)

    # =====================================================
    # GEMINI
    # =====================================================

    with st.chat_message("assistant"):

        answer = None

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=MODEL,
                    contents=full_prompt
                )

                answer = response.text

                break

            except Exception as e:

                if attempt < 2:

                    time.sleep(2)

                else:

                    error_text = str(e)

                    if "503" in error_text:

                        answer = (
                            "Kaze is temporarily busy. "
                            "Please try again in a moment."
                        )

                    elif "429" in error_text:

                        answer = (
                            "Kaze is temporarily rate-limited. "
                            "Please try again shortly."
                        )

                    else:

                        answer = (
                            "Something went wrong. "
                            "Please try again."
                        )

        st.markdown(answer)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
