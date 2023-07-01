import requests
import streamlit as st
from streamlit_chat import message


class ChatbotApp:
    """
    A class for creating frontend Streamlit Chatbot.
    """

    def __init__(self) -> None:
        self.initialize_session_state()

    def initialize_session_state(self) -> None:
        """
        Initialize the session state variables if not already present.
        """

        if 'openai_api_key' not in st.session_state:
            st.session_state['openai_api_key'] = ''
        if 'db_path' not in st.session_state:
            st.session_state['db_path'] = ''
        if 'db_name' not in st.session_state:
            st.session_state['db_name'] = "vector_db.pkl"
        if 'current_files' not in st.session_state:
            st.session_state['current_files'] = ''
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [{"role": "assistant", "content": "Hi, How can I help you?"}]
        if 'user_input' not in st.session_state:
            st.session_state['user_input'] = None


    def process_uploaded_pdf(self, uploaded_files: list[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
        """
        Process the uploaded PDF file, dump it, and create a vector DB.
        
        Args:
            uploaded_files (UploadedFile): The uploaded PDF files.
        """

        files_names = sorted([file.name for file in uploaded_files])
        for uploaded_file in uploaded_files:
            requests.post(
                "http://backend_llm_pdf:8000/dump_pdf",
                files={
                    'pdf_bytes': (
                        uploaded_file.name,
                        uploaded_file.read(),
                        'application/pdf'
                    )
                },
                timeout=100
            )

        st.session_state.db_path = requests.post(
            "http://backend_llm_pdf:8000/create_vec_db",
            json={
                "openai_key": st.session_state.openai_api_key,
                "file_names": files_names,
                "db_name": st.session_state.db_name
            },
            timeout=100
        ).json()['DB_PATH']

        st.session_state.current_files = files_names
        st.session_state.user_input = None


    def app(self) -> None:
        """
        Run the chatbot application.
        """

        with st.sidebar:
            self.display_sidebar()

        st.title("💬 PDF Q&A Chatbot")
        with st.form("chat_input", clear_on_submit=True):
            a, b = st.columns([4, 1])
            user_input = a.text_input(
                label="Your message:",
                placeholder="What would you like to ask?",
                label_visibility="collapsed",
            )
            st.session_state.user_input = None if st.session_state.user_input == user_input else user_input
            b.form_submit_button("Send", use_container_width=True)

        for i, msg in enumerate(st.session_state.messages):
            message(msg["content"], is_user=msg["role"] == "user", key=f"history_{i+1}", allow_html=True)

        if st.session_state.user_input and not st.session_state.openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.session_state.user_input = None

        if st.session_state.user_input and st.session_state.openai_api_key and st.session_state.db_path:
            st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
            message(st.session_state.user_input, is_user=True, key="question", allow_html=True)

            answer = self.get_chatbot_answer()
            answer = f"""<p>{"I don't know." if "I don't know." in answer.json()["answer"] else answer.json()["answer"]}</p>
            <p>Sources: <em>{"N/A" if "I don't know." in answer.json()["answer"] else answer.json()["sources"]}</em></p>
            """
            st.session_state.messages.append({"role": "assistant", "content": answer})
            message(answer, key="answer", allow_html=True)


    def display_sidebar(self) -> None:
        """
        Display the sidebar containing the OpenAI API key input and PDF file uploader.
        """
        st.session_state.openai_api_key = st.text_input(
            'OpenAI API Key',
            key='chatbot_api_key',
            type='password'
        )

        if st.session_state.openai_api_key:
            uploaded_files = st.file_uploader(
                "Upload a PDF file",
                type="pdf",
                accept_multiple_files=True
            )

            if uploaded_files and st.session_state.current_files != sorted([file.name for file in uploaded_files]):
                self.process_uploaded_pdf(uploaded_files)


    def get_chatbot_answer(self) -> requests.Response:
        """
        Retrieve the chatbot's answer from the backend.

        Returns:
            The response object containing the chatbot's answer.
        """

        answer = requests.post(
            "http://backend_llm_pdf:8000/get_answer",
            json={
                "openai_key": st.session_state.openai_api_key,
                "db_path": st.session_state.db_path,
                "k": 3,
                "question": st.session_state.user_input,
            },
            timeout=100
        )
        return answer


if __name__ == '__main__':
    chatbot_app = ChatbotApp()
    chatbot_app.app()
