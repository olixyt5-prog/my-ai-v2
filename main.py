```python
import streamlit as st
import time
from google import genai

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Kaze AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# GEMINI SETUP
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    MODEL = "gemini-3.8-flash"

except Exception as e:
    st.error("Kaze setup error:")
    st.code(str(e))
    st.stop()

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    try:
        st.session_state.chat = client.chats.create(
            model=MODEL
        )
    except Exception as e:
        st.error("Could not start Kaze:")
        st.code(str(e))
        st.stop()

# -----------------------------
# CSS
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
    padding-bottom: 50px;
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

        try:
            st.session_state.chat = client.chats.create(
                model=MODEL
            )
        except Exception as e:
            st.error(str(e))

        st.rerun()

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []

        try:
            st.session_state.chat = client.chats.create(
                model=MODEL
            )
        except Exception as e:
            st.error(str(e))

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
# DISPLAY CHAT
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
prompt = st.chat_input("Message Kaze...")

if prompt:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Kaze response
    with st.chat_message("assistant"):

        thinking = st.empty()

        thinking.markdown("🧠 Kaze is thinking...")

        start_time = time.time()

        try:

            response = st.session_state.chat.send_message(
                message=prompt
            )

            answer = response.text

            # Make thinking message visible briefly
            elapsed = time.time() - start_time

            if elapsed < 0.7:
                time.sleep(0.7 - elapsed)

            thinking.empty()

            st.markdown(answer)

        except Exception as e:

            thinking.empty()

            # SHOW REAL ERROR
            st.error("Kaze couldn't answer.")

            st.write("### 🔍 Actual error:")
            st.code(str(e))

            answer = "I couldn't answer that message."

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
```

### Then do this

1. Save `main.py`
2. Push/commit it to your GitHub repo.
3. Let Streamlit redeploy.
4. Send Kaze **one message**.
5. Send a **second message**.
6. If it fails, you'll now see something like:

   * `429 RESOURCE_EXHAUSTED`
   * `403 PERMISSION_DENIED`
   * `400 INVALID_ARGUMENT`
   * or another specific error.

**Don't send me your API key.** Just send me the **actual error text shown under “🔍 Actual error:”**.

That will tell us exactly what's breaking instead of guessing. Google specifically recommends checking the actual API error code; for example, `429` means a rate/resource limit situation and should be handled differently from `400`/`403` errors.
