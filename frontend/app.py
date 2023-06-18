import openai
import streamlit as st
from streamlit_chat import message
import requests

# Helper class for session state
class SessionState:
    def __init__(self):
        self.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Create an instance of SessionState
state = SessionState()

# Create a layout with two columns: sidebar and file upload window
with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key', key='chatbot_api_key', type='password')
    
with st.sidebar:

    uploaded_files = st.file_uploader("Upload a PDF file", type="pdf", accept_multiple_files=True)

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # Process each uploaded PDF file
            pdf_contents = uploaded_file.read()
            # TODO: Add your code to process the PDF contents here

st.title("💬 Streamlit GPT")

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for msg in state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    
if user_input and openai_api_key:
    openai.api_key = openai_api_key
    state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    # Call the FastAPI endpoint to get a response
    response = requests.get("http://127.0.0.1:8000")  # Replace with the appropriate URL of your FastAPI server
    state.messages.append({"role": "assistant", "content": response.json()["message"]})
    message(response.json()["message"])

