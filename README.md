# Code Review Assistant

This is a simple Streamlit app that allows you to upload code or paste it into a text area and receive an AI-powered review. The app uses the Mistral model running locally via Ollama instead of OpenAI.

## Requirements
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/) (for running Mistral locally)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setting up Mistral with Ollama
1. **Install Ollama**
   - Follow the instructions at [Ollama's website](https://ollama.com/download) to install Ollama for your OS.

2. **Pull the Mistral model**
   ```sh
   ollama pull mistral
   ```

3. **Start the Ollama server**
   ```sh
   ollama serve
   ```
   By default, Ollama serves the API at `http://localhost:11434`.

## Running the App

1.  create fresh environment
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate   # on Mac
    ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Streamlit app:
   ```sh
   streamlit run app.py
   ```

## Using the App
- Paste your code in the text area or upload a `.py` or `.java` file.
- Click "Run Review" to get feedback from the Mistral model running locally.

## Notes
- No OpenAI API key is required. The app connects to your local Ollama instance.
- Make sure Ollama is running and the Mistral model is available before using the app.
