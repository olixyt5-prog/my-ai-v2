import streamlit as st
import time
from google import genai

st.set_page_config(
    page_title="Kaze AI",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# API KEY
# -----------------------------

api_key = st.secrets["GEMINI_API_KEY"]

MODEL = "gemini-3.8-flash"


# -----------------------------
# CHAT HISTORY
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# STYLE
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: white;
}

.kaze-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid #eeeeee;
}

.kaze-logo {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: #111111;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 20px;
}

.kaze-name {
    font-size: 22px;
    font-weight: 700;
}

.kaze-subtitle {
    color: #888888;
    font-weight: 400;
}

.welcome {
    text-align: center;
    padding-top: 130px;
}

.welcome h1 {
    font-size: 38px;
    margin-bottom: 8px;
}

.welcome p {
    color: #777777;
    font-size: 17px;

}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.markdown("""
<div class="kaze-header">
    <div class="kaze-logo">K</div>

    <div class="kaze-name">
        Kaze <span class="kaze-subtitle">AI</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("Kaze AI")

    if st.button("＋ New chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


    if st.button("Clear chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


    st.divider()

    st.caption("Powered by Gemini")


# -----------------------------
# WELCOME
# -----------------------------

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">
        <h1>How can I help you?</h1>
        <p>Ask Kaze anything.</p>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# SHOW CHAT
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# INPUT
# -----------------------------

prompt = st.chat_input("Message Kaze...")


if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # Show user message
    with st.chat_message("user"):

        st.markdown(prompt)


    # Kaze
    with st.chat_message("assistant"):

        thinking = st.empty()

        thinking.markdown("🧠 Kaze is thinking...")

        start_time = time.time()


        try:

            # Create a NEW client for this request
            client = genai.Client(
                api_key=api_key
            )


            # Build conversation context
            conversation = ""

            for message in st.session_state.messages:

                if message["role"] == "user":

                    conversation += (
                        "User: "
                        + message["content"]
                        + "\n"
                    )

                else:

                    conversation += (
                        "Kaze: "
                        + message["content"]
                        + "\n"
                    )


            conversation += "Kaze:"


            # Send request
            response = client.models.generate_content(
                model=MODEL,
                contents=conversation
            )


            answer = response.text


            # Keep thinking visible briefly
            elapsed = time.time() - start_time

            if elapsed < 0.7:

                time.sleep(0.7 - elapsed)


            thinking.empty()

            st.markdown(answer)


        except Exception as e:

            thinking.empty()

            st.error("Kaze couldn't answer.")

            st.write("### Actual error:")

            st.code(str(e))

            answer = "I couldn't answer that message."


        # Save Kaze response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
