FROM python:3.8

COPY ./ ./

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

EXPOSE 8501

CMD streamlit run app.py