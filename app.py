import streamlit as st
import os
from dotenv import load_dotenv 

import requests

MAX_CHARS = 4000

def get_code_feedback(code):
    prompt = f"""
    You are a helpful and friendly code review assistant.

    Review the following code that could be written in Python or Java and give feedback in four clearly labeled sections:
    1. **Language**: Display the code language.
    2. **Style**: Comment on formatting, naming and structure.
    3. **Errors**: Point out any bug or mistake.
    4. **Clarity**: Suggests ways to make the code easier to understand.

    Keep it short. The entire response shouldnot exceed 30 lines.

    Here is the code:
    
    {code}
    """

    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=150)
        response.raise_for_status()
        data = response.json()
        # Ollama returns the response in 'message' or 'choices', depending on version
        if "message" in data:
            return data["message"]["content"]
        elif "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return "No response from Mistral."
    except Exception as e:
        return f"Error communicating with Mistral/Ollama: {e}"



st.set_page_config(page_title="Code Review Assistant", layout="wide")
st.title("Code Review Assistant")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Paste your code")
    with st.form("code_review_form"):
        code_input = st.text_area("Your code here", height=300, key="code_input")
        uploaded_file = st.file_uploader("Or upload a file ", type=["java", "py"], key="file_uploader")
        file_content = ""
        if uploaded_file is not None:
            try:
                file_content = uploaded_file.read().decode("utf-8")
                st.text_area("File content", file_content, height=300, key="file_content")
            except Exception:
                st.error("Error uploading file. Please upload a valid file")
        # Prefer file content if uploaded, else text area
        code_to_review = file_content if file_content else code_input
        submitted = st.form_submit_button("Run Review")
        if submitted:
            if not code_to_review.strip():
                st.warning("⚠️ Please paste or upload some code.")
            elif len(code_to_review) > MAX_CHARS:
                st.error(f"🚫 This code is too long. Keep it under {MAX_CHARS} chars.")
            else:
                with st.spinner("Reviewing your code..."):
                    try:
                        feedback = get_code_feedback(code_to_review)
                        st.session_state["feedback"] = feedback
                    except Exception as e:
                        st.error(f"💥 Opps! Something went wrong!")

with col2:
    st.subheader("🔍 Review Output")
    if st.session_state.get("feedback"):
        st.markdown("### AI Code Review")
        st.markdown(st.session_state["feedback"])
    elif st.session_state.get("code_input"):
        st.write("Review will appear here")
    else:
        st.write("Past some code to get started")
   