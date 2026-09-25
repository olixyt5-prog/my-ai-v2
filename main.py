import streamlit as st
from google import genai

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Kaze AI",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GEMINI SETUP
# =========================================================

api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

.stApp {
    background: #080809;
    color: #f5f5f5;
}

.block-container {
    max-width: 950px;
    padding-top: 1rem;
    padding-bottom: 120px;
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

/* ---------- TOP BAR ---------- */

.kaze-header {
    height: 55px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid rgba(255,255,255,0.06);

    margin-bottom: 20px;
}

.kaze-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.kaze-logo {
    width: 30px;
    height: 30px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background: #f1f1f1;
    color: #080809;

    font-weight: 700;
    font-size: 14px;
}

.kaze-title {
    font-size: 17px;
    font-weight: 600;
    color: #eeeeee;
}

.kaze-ai {
    color: #666666;
    font-size: 11px;
    margin-left: 4px;
}

/* ---------- WELCOME ---------- */

.welcome {
    text-align: center;

    padding-top: 100px;
    padding-bottom: 70px;
}

.welcome-small {
    color: #777777;
    font-size: 13px;
    margin-bottom: 15px;
}

.welcome-title {
    font-size: 48px;
    font-weight: 600;

    letter-spacing: -2.5px;

    color: #f5f5f5;

    margin-bottom: 12px;
}

.welcome-subtitle {
    color: #707070;
    font-size: 14px;
}

/* ---------- SUGGESTION CARDS ---------- */

.cards {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 10px;

    max-width: 800px;

    margin: 40px auto 0 auto;
}

.card {
    text-align: left;

    padding: 16px;

    border-radius: 15px;

    border: 1px solid rgba(255,255,255,0.07);

    background: rgba(255,255,255,0.025);

    transition: all 0.2s ease;
}

.card:hover {
    background: rgba(255,255,255,0.05);

    border-color:
        rgba(255,255,255,0.12);

    transform: translateY(-2px);
}

.card-icon {
    font-size: 16px;
    margin-bottom: 10px;
}

.card-title {
    font-size: 13px;
    font-weight: 500;
    color: #dddddd;
}

.card-description {
    color: #666666;
    font-size: 11px;
    margin-top: 5px;
}

/* ---------- CHAT ---------- */

[data-testid="stChatMessage"] {
    background: transparent !important;

    border: none !important;

    padding-top: 12px;
    padding-bottom: 12px;
}

/* Assistant message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: rgba(255,255,255,0.025) !important;

    border-radius: 18px !important;

    padding: 16px !important;

    margin-bottom: 8px;
}

/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: transparent !important;
}

/* Chat text */

[data-testid="stChatMessage"] p {
    font-size: 14px;
    line-height: 1.7;
}

/* ---------- CHAT INPUT ---------- */

[data-testid="stChatInput"] {
    border-top: none !important;
}

[data-testid="stChatInput"] > div {
    background: #151517 !important;

    border:
        1px solid
        rgba(255,255,255,0.09) !important;

    border-radius: 18px !important;

    box-shadow:
        0 15px 50px
        rgba(0,0,0,0.35) !important;
}

[data-testid="stChatInput"] textarea {
    color: #eeeeee !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #666666 !important;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #0b0b0d;
    border-right:
        1px solid
        rgba(255,255,255,0.06);
}

.sidebar-heading {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
}

.sidebar-description {
    color: #666666;
    font-size: 12px;
    line-height: 1.6;
}

/* ---------- MOBILE ---------- */

@media (max-width: 700px) {

    .welcome {
        padding-top: 70px;
    }

    .welcome-title {
        font-size: 38px;
    }

    .cards {
        grid-template-columns: repeat(2, 1fr);
    }

}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="kaze-header">

    <div class="kaze-brand">

        <div class="kaze-logo">
            K
        </div>

        <div class="kaze-title">
            Kaze
            <span class="kaze-ai">AI</span>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-heading">Kaze</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div class="sidebar-description">

        Kaze is your AI assistant.

        <br><br>

        Ask questions, write code,
        brainstorm ideas, or learn
        something new.

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.messages:

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

        <div class="cards">

            <div class="card">

                <div class="card-icon">
                    ✦
                </div>

                <div class="card-title">
                    Ideas
                </div>

                <div class="card-description">
                    Brainstorm something new
                </div>

            </div>


            <div class="card">

                <div class="card-icon">
                    &lt;/&gt;
                </div>

                <div class="card-title">
                    Code
                </div>

                <div class="card-description">
                    Build and debug projects
                </div>

            </div>


            <div class="card">

                <div class="card-icon">
                    ◌
                </div>

                <div class="card-title">
                    Learn
                </div>

                <div class="card-description">
                    Understand difficult topics
                </div>

            </div>


            <div class="card">

                <div class="card-icon">
                    ↗
                </div>

                <div class="card-title">
                    Create
                </div>

                <div class="card-description">
                    Turn ideas into reality
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask Kaze anything..."
)

if prompt:

    # -------------------------
    # Add user message
    # -------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # -------------------------
    # Show user message
    # -------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

    # -------------------------
    # Prepare conversation
    # -------------------------

    conversation = []

    for message in st.session_state.messages:

        role = message["role"].upper()

        content = message["content"]

        conversation.append(
            f"{role}: {content}"
        )

    full_prompt = "\n\n".join(
        conversation
    )

    # -------------------------
    # Ask Gemini
    # -------------------------

    with st.chat_message("assistant"):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=full_prompt
            )

            answer = response.text

            st.markdown(answer)

        except Exception as e:

            answer = (
                "Sorry, something went wrong.\n\n"
                f"`{e}`"
            )

            st.markdown(answer)

    # -------------------------
    # Save response
    # -------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
