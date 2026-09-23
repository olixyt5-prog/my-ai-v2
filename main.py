import streamlit as st

# 1. Page Configuration & Title
st.set_page_config(page_title="My Classroom AI", page_icon="🧠")
st.title("🧠 My Custom Classroom AI")
st.write("Type a sentence below to see my AI analyze your emotions live!")

# 2. Main Text Input Box
user_input = st.text_input("Type something here:", placeholder="Today is an awesome day!")

# 3. The Upgraded AI Brain (Rule-Based NLP Logic)
def custom_ai_brain(text):
    text = text.lower()
    
    # 🚨 CUSTOM WORD BANKS (You can add your own words inside these brackets!)
    positive = ["good", "great", "happy", "awesome", "love", "cool", "best", "fire", "goated", "clutch"]
    negative = ["bad", "sad", "angry", "hate", "terrible", "boring", "tired", "cooked", "mid", "L"]
    school = ["school", "class", "teacher", "math", "science", "history", "english", "homework", "principal"]
    
    # AI Decision Making Tree
    if any(word in text for word in school):
        return "Academic Focus Mode! 📚", "blue"
    elif any(word in text for word in positive):
        return "Positive Mood! ✨", "green"
    elif any(word in text for word in negative):
        return "Negative Mood. 😢", "red"
    elif text == "":
        return "Awaiting Input...", "gray"
    else:
        return "Neutral Mood. 😐", "orange"

# 4. Process and Display Results on the Website
status, color = custom_ai_brain(user_input)

if user_input:
    st.subheader("AI Result:")
    if color == "blue":       st.info(status)
    elif color == "green":    st.success(status)
    elif color == "red":      st.error(status)
    else:                     st.warning(status)
