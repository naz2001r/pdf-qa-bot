# PDF Q&A Chatbot

This is a PDF Chatbot application that utilizes the power of OpenAI's GPT3.5-turbo model. The chatbot is designed to interact with users and provide helpful information related to PDF files. It has a backend built with FastAPI and a frontend built with Streamlit. The entire application is containerized using Docker Compose for easy deployment and scalability.

## Features

- Conversational interface: The chatbot interacts with users in a natural language conversation style, allowing them to ask questions and get relevant responses related to PDF files.
- Backend API: The backend is built with FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.10+.
- Frontend Interface: The frontend is developed using Streamlit, a powerful Python library for building interactive web applications for data science and machine learning.
- Docker Compose: The application is containerized using Docker Compose, allowing for easy deployment and management of the entire stack.

## Requirements

- Docker: Ensure that Docker is installed on your system. Refer to the official Docker documentation for installation instructions specific to your operating system.

## Installation and Usage

1. Clone the repository:

   ```
   $ git clone https://github.com/naz2001r/pdf-qa-bot.git
   $ cd pdf-qa-bot
   ```

2. Build and run the Docker containers using Docker Compose:

   ```
   $ docker-compose up -d
   ```

   This command will build the necessary Docker images and start the containers in detached mode.

3. Access the application:

   - Backend API: The FastAPI backend will be available at `http://0.0.0.0:8000`. You can interact with the API directly at `http://0.0.0.0:8000/docs`.
   - Frontend UI: The Streamlit frontend will be available at `http://localhost:8501`. Open this URL in your web browser to access the chatbot interface.

4. Interact with the PDF Chatbot:

   - Open the Streamlit interface in your web browser at `http://localhost:8501`.
   - Write OpenAI API Key
   - Load one or more PDF files.
   - Start a conversation with the chatbot by typing your questions related to PDF files.
   - The chatbot will process your input and provide relevant responses based on the GPT3.5-turbo model's capabilities.

5. Stop the application:

   To stop the running Docker containers, use the following command:

   ```
   $ docker-compose down
   ```

   This will stop and remove the containers, but your data and configuration will be preserved for future use.

## Customization

You can customize and extend the PDF Chatbot application according to your requirements. Here are a few possible enhancements:

- Improve PDF file operations: Expand the functionality of the chatbot to support more advanced operations on PDF files, such as summarization, extracting specific pages or specific elements such as tables.
- UI improvements: Customize the Streamlit frontend to match your desired visual aesthetics and user experience.
- Security: Implement authentication and access control mechanisms to secure the application.

Feel free to explore the codebase and make changes as needed to suit your use case.

## License

The PDF Chatbot application is licensed under the [Apache License](LICENSE).

## Acknowledgments

- This application utilizes the power of OpenAI's GPT3.5-turbo model. Visit the [OpenAI website](https://openai.com) for more information on their technology.
- The backend API is built with FastAPI, a fantastic Python web framework. Check out the [FastAPI documentation](https://fastapi.tiangolo.com/) to learn more about its features and capabilities.
- The frontend interface is developed using Streamlit, an amazing library for building interactive web applications with Python. Explore the [Streamlit documentation](https://docs.streamlit.io/) to discover its functionalities.

## Support

If you encounter any issues or have any questions or suggestions regarding the PDF Q&A Chatbot application, please open an issue on the GitHub repository: [https://github.com/naz2001r/pdf-qa-bot](https://github.com/naz2001r/pdf-qa-bot).

Your feedback and contributions are highly appreciated!
