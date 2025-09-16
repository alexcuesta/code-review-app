import streamlit as st
import os
from dotenv import load_dotenv 

import requests

def get_code_feedback(code):
    prompt = f"Review the following code, detect the language and give feedback on style, idiomacy, errors and clarity:\n\n{code}"
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
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
    st.subheader("Paste your code")
    code_input = st.text_area("Your code here", height=300)
with col2:
    st.subheader("Review Output")

    if st.session_state.get("feedback"):
        st.markdown("### AI Code Review")
        st.markdown(st.session_state["feedback"])
    elif code_input:
        st.write("Review will appear here")
    else:
        st.write("Paset some code to get started")

uploaded_file = st.file_uploader("Or upload a file ", type=["java", "py"])

if uploaded_file is not None:
    try:
        code_input = uploaded_file.read().decode("utf-8")
        st.text_area("File content", code_input, height=300)
    except Exception:
        st.error("Error uploading file. Please upload a valid file")

if code_input:
    if st.button("Run Review"):
        with st.spinner("Reviewing your code..."):
            feedback = get_code_feedback(code_input)
            st.session_state["feedback"] = feedback
    st.rerun()