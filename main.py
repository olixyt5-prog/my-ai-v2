import streamlit as st
from google import genai

# 1. Page Configuration & Setup
st.set_page_config(page_title="My Omni-AI Brain", page_icon="🤖")
st.title("🤖 My Custom Omni-AI Brain")
st.write("Ask my AI absolutely anything in the world!")

# 2. Securely Insert Your Secret Key 
# Delete the text inside the quotes below and paste your copied key!
API_KEY = "AQ.Ab8RN6JMMcN9-uXx0whShqQrMVNSktkHuWpSWaCHblHfN0hnCw"

# Initialize the real AI engine
client = genai.Client(api_key=API_KEY)

# 3. Main Text Input Box
user_query = st.text_input("Ask a question:", placeholder="Why is the sky blue?")

# 4. Generate the Response
if user_query:
    with st.spinner("AI Brain thinking... 🧠"):
        try:
            # Tell the supercomputer brain to answer your question
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_query,
            )
            
            st.subheader("AI Answer:")
            st.write(response.text)
            
        except Exception as e:
            st.error("Oops! Make sure you pasted your correct API Key inside the code.")

