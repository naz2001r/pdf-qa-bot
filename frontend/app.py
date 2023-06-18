import requests
import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html


if 'openai_api_key' not in st.session_state: st.session_state['openai_api_key']=''
if 'db_path' not in st.session_state: st.session_state['db_path']=''
if 'db_name' not in st.session_state: st.session_state['db_name']="vector_db.pkl"
if 'current_file' not in st.session_state: st.session_state['current_file']=''
if 'messages' not in st.session_state: st.session_state['messages']=[{"role": "assistant", "content": "Hi, How can I help you?"}]
if 'user_input' not in st.session_state: st.session_state['user_input']=None

def app():
    # Create a layout with two columns: sidebar and file upload window
    with st.sidebar :
        st.session_state.openai_api_key = st.text_input('OpenAI API Key', key='chatbot_api_key', type='password')

        # TODO: add suport of multiple files
        # TODO: add logging
        if st.session_state.openai_api_key:
            uploaded_file = st.file_uploader("Upload a PDF file", 
                                             type="pdf", 
                                             accept_multiple_files=False)

            if uploaded_file and st.session_state.current_file != uploaded_file.name:
                # Process uploaded PDF file
                r = requests.post("http://backend_llm_pdf:8000/dump_pdf", 
                    files={
                        'pdf_bytes': (uploaded_file.name, uploaded_file.read(), 'application/pdf')
                    }
                )

                st.session_state.db_path = requests.post("http://backend_llm_pdf:8000/create_vec_db", 
                    json={
                        "openai_key": st.session_state.openai_api_key,
                        "file_name": uploaded_file.name,
                        "db_name": st.session_state.db_name
                    }
                ).json()['DB_PATH']

                st.session_state.current_file = uploaded_file.name
                st.session_state.user_input = None
                
    st.title("💬 PDF Q&A Chatbot")
    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])
        user_input = a.text_input(
            label="Your message:",
            placeholder="What would you like to ask?",
            label_visibility="collapsed",
        )
        st.session_state.user_input = None if st.session_state.user_input==user_input else user_input
        b.form_submit_button("Send", use_container_width=True)

    for i, msg in enumerate(st.session_state.messages):
        message(msg["content"], is_user=msg["role"] == "user", key=f"history_{i+1}")

    if st.session_state.user_input and not st.session_state.openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.session_state.user_input = None
        
    if st.session_state.user_input and st.session_state.openai_api_key and st.session_state.db_path:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        message(st.session_state.user_input, is_user=True, key="question")

        # Call backend to get chatbot answer
        answer = requests.post("http://backend_llm_pdf:8000/get_answer",
                                json={
                                    "openai_key": st.session_state.openai_api_key,
                                    "db_path": st.session_state.db_path,
                                    "k": 3,
                                    "question": st.session_state.user_input,
                                }
        )
        answer = """
        My Answer:{answer}
        SOURCES: {source}
        """.format(
            answer=answer.json()["answer"],
            source=answer.json()["sources"]
        )
        st.session_state.messages.append({"role": "assistant", "content": answer})
        message(answer, key="answer")
        

if __name__ == '__main__':
    app()
