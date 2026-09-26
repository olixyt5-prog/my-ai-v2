import streamlit as st
import time
import re
import ast
import operator
from google import genai

# =========================================================
# KAZE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Kaze AI",
    page_icon="🧠",
    layout="wide"
)

MODEL = "gemini-3.8-flash"

api_key = st.secrets["GEMINI_API_KEY"]


# =========================================================
# SAFE CALCULATOR
# =========================================================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv
}


def calculate_expression(expression):

    expression = expression.replace(",", "")
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate_node(tree.body)

    except Exception:
        return None


def evaluate_node(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError()

    if isinstance(node, ast.BinOp):

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operation = operators.get(type(node.op))

        if operation is None:
            raise ValueError()

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        value = evaluate_node(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

    raise ValueError()


def try_calculate(text):

    cleaned = text.strip()

    pattern = r"^[\d\s\+\-\*\/\%\(\)\.\,\×\÷]+$"

    if re.fullmatch(pattern, cleaned):

        result = calculate_expression(cleaned)

        if result is not None:
            return result

    return None


# =========================================================
# SESSION MEMORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# KAZE PERSONALITY / REASONING INSTRUCTIONS
# =========================================================

SYSTEM_PROMPT = """
You are Kaze, a highly capable AI assistant.

Your job is to give accurate, useful and intelligent answers.

IMPORTANT RULES:

1. Think carefully before answering.
2. Do not invent facts.
3. If you are uncertain, clearly say so.
4. For difficult questions, break the problem into smaller parts.
5. For mathematics, prioritize exact answers.
6. For programming, provide working code and explain important parts.
7. When the user is a beginner, explain complicated things simply.
8. Remember the conversation and use previous messages when relevant.
9. Do not repeat the user's question unnecessarily.
10. Give the direct answer first, then explanation when useful.
11. For large calculations, trust the calculator result supplied by the application.
12. Never claim to have performed an action that you did not actually perform.
13. Be friendly and natural, not robotic.

You are Kaze AI.
"""


# =========================================================
# STYLING
# =========================================================

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


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="kaze-header">
    <div class="kaze-logo">K</div>

    <div class="kaze-name">
        Kaze <span class="kaze-subtitle">AI</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("Kaze AI")

    if st.button("＋ New chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


    if st.button("Clear chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


    st.divider()

    st.caption("Kaze Smart Mode 🧠")


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">
        <h1>How can I help you?</h1>
        <p>Ask Kaze anything.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# DISPLAY CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

prompt = st.chat_input("Message Kaze...")


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    with st.chat_message("user"):

        st.markdown(prompt)


    with st.chat_message("assistant"):

        thinking = st.empty()

        thinking.markdown("🧠 Kaze is thinking...")

        start_time = time.time()


        try:

            # -------------------------------------------------
            # EXACT CALCULATOR
            # -------------------------------------------------

            calculation = try_calculate(prompt)

            if calculation is not None:

                answer = str(calculation)

            else:

                # -------------------------------------------------
                # GEMINI
                # -------------------------------------------------

                client = genai.Client(
                    api_key=api_key
                )


                conversation = SYSTEM_PROMPT + "\n\n"

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


                conversation += "\nKaze:"


                response = client.models.generate_content(
                    model=MODEL,
                    contents=conversation
                )


                answer = response.text


            elapsed = time.time() - start_time

            if elapsed < 0.7:

                time.sleep(0.7 - elapsed)


            thinking.empty()

            st.markdown(answer)


        except Exception as e:

            thinking.empty()

            error_text = str(e)

            if "429" in error_text:

                answer = (
                    "🧠 Kaze has reached the current Gemini "
                    "free-tier request limit. The code is working, "
                    "but the AI service needs its quota to reset."
                )

            else:

                answer = "Kaze ran into an error."

                st.code(error_text)


            st.markdown(answer)


    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
