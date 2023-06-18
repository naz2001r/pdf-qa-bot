FROM python:3.10-slim
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt

EXPOSE 8501
CMD streamlit run --server.port 8501 --browser.gatherUsageStats false --server.enableWebsocketCompression true app.py