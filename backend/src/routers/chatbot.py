import os
import io
from langchain import OpenAI
from fastapi import APIRouter, UploadFile, File
from langchain.chains import RetrievalQAWithSourcesChain

try:
    from src.models import *
    from src.pdf_loader import PdfToTextLoader
    from src.vec_db import VectorizeDB
except:
    from backend.src.models import *
    from backend.src.pdf_loader import PdfToTextLoader
    from backend.src.vec_db import VectorizeDB


chatbot_router = APIRouter()

@chatbot_router.post("/dump_pdf", tags=['Chatbot'])
def dump_pdf(pdf_bytes:UploadFile = File(None)):
    with open(pdf_bytes.filename, 'wb') as file:
        file.write(pdf_bytes.file.read())
    return {
        "Status": 200
    }

@chatbot_router.post("/create_vec_db", tags = ['Chatbot'])
def create_vec_db(data:PDFObject):
    # must return path to created db
    # save pdf in backend part

    # pdf preprocessing
    pdf_loader = PdfToTextLoader(data.file_name)
    pdf_texts = pdf_loader.load_single_pdf()
    pages = pdf_loader.text_to_docs(pdf_texts)

    # creating db
    db = VectorizeDB(data.openai_key)
    db.vectorize(pages)
    db.dump_db(data.db_name)

    return {
        "DB_PATH": data.db_name
    }

# TODO: create get answer
@chatbot_router.get("/get_answer", tags = ['Chatbot'])
def get_answer(openai_api_key, question):
    # load db
    # set retriver
    retriever = '' # load
    chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0,openai_api_key=openai_api_key), chain_type="stuff", retriever=retriever)
    return chain({"question": question}, return_only_outputs=True)

