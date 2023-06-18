import os
import io
from langchain import OpenAI
from fastapi import APIRouter, UploadFile, File
from langchain.chains import RetrievalQAWithSourcesChain

try:
    from src.models import *
    from src.pdf_loader import PdfToTextLoader
    from src.vec_db import VectorizeDB
    from src.constants import ROOT_DATA, ROOT_DB
except:
    from backend.src.models import *
    from backend.src.pdf_loader import PdfToTextLoader
    from backend.src.vec_db import VectorizeDB
    from backend.src.constants import ROOT_DATA, ROOT_DB


chatbot_router = APIRouter()

@chatbot_router.post("/dump_pdf", tags=['Chatbot'])
def dump_pdf(pdf_bytes:UploadFile = File(None)) -> dict:

    os.makedirs(ROOT_DATA, exist_ok=True)
    with open(os.path.join(ROOT_DATA,pdf_bytes.filename), 'wb') as file:
        file.write(pdf_bytes.file.read())
    return {
        "Status": 200
    }

@chatbot_router.post("/create_vec_db", tags = ['Chatbot'])
def create_vec_db(data:PDFObject) -> dict:

    # pdf preprocessing
    pdf_loader = PdfToTextLoader(os.path.join(ROOT_DATA, data.file_name))
    pdf_texts = pdf_loader.load_single_pdf()
    pages = pdf_loader.text_to_docs(pdf_texts)

    # create folder for db
    os.makedirs(ROOT_DB, exist_ok=True)
    db_path = os.path.join(ROOT_DB, data.db_name)

    # creating db
    db = VectorizeDB(data.openai_key)
    db.vectorize(pages)
    db.dump_db(db_path)

    return {
        "DB_PATH": db_path
    }


@chatbot_router.post("/get_answer", tags = ['Chatbot'])
def get_answer(data: QueryObject) -> dict:
    # load db
    db = VectorizeDB.load_db(data.db_path)
    db.retriver = data.k

    # create PDF QA retrieval
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        OpenAI(
            temperature=0,
            openai_api_key=data.openai_key
        ), 
        chain_type="stuff", 
        retriever=db.retriver
    )
    return chain({"question": data.question}, return_only_outputs=data.return_only_outputs)

