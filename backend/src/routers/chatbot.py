import os
from fastapi import APIRouter, UploadFile, File
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain

try:
    from src.models import PDFObject, QueryObject
    from src.pdf_loader import PdfToTextLoader
    from src.vec_db import VectorizeDB
    from src.constants import ROOT_DATA, ROOT_DB
except ImportError:
    from backend.src.models import PDFObject, QueryObject
    from backend.src.pdf_loader import PdfToTextLoader
    from backend.src.vec_db import VectorizeDB
    from backend.src.constants import ROOT_DATA, ROOT_DB


chatbot_router = APIRouter()


@chatbot_router.post("/dump_pdf", tags=['Chatbot'])
def dump_pdf(pdf_bytes: UploadFile = File(None)) -> dict:
    """
    Dump a PDF file to the data folder.

    Args:
        pdf_bytes (UploadFile): PDF file to be dumped.

    Returns:
        dict: Status 200 if successful.
    """

    os.makedirs(ROOT_DATA, exist_ok=True)
    with open(os.path.join(ROOT_DATA, pdf_bytes.filename), 'wb') as file:
        file.write(pdf_bytes.file.read())
    return {
        "Status": 200
    }


@chatbot_router.post("/create_vec_db", tags=['Chatbot'])
def create_vec_db(data: PDFObject) -> dict:
    """
    Create a vector database from a PDF files.

    Args:
        data (PDFObject): Object containing PDF information.

    Returns:
        dict: Dictionary containing the path to the created vector database.
    """

    # PDF preprocessing
    pages = []
    for file_name in data.file_names:
        pdf_loader = PdfToTextLoader(os.path.join(ROOT_DATA, file_name))
        pdf_texts = pdf_loader.load_single_pdf()
        pages.extend(pdf_loader.text_to_docs(pdf_texts))

    # Create folder for database
    os.makedirs(ROOT_DB, exist_ok=True)
    db_path = os.path.join(ROOT_DB, data.db_name)

    # Creating the vector database
    vector_db = VectorizeDB(data.openai_key)
    vector_db.vectorize(pages)
    vector_db.dump_db(db_path)

    return {
        "DB_PATH": db_path
    }


@chatbot_router.post("/get_answer", tags=['Chatbot'])
def get_answer(data: QueryObject) -> dict:
    """
    Get an answer from the vector database.

    Args:
        data (QueryObject): Object containing query information.

    Returns:
        dict: Dictionary containing the answer.
    """

    # Load the vector database
    vector_db = VectorizeDB.load_db(data.db_path)
    vector_db.retriever = data.k

    # Create PDF QA retrieval
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        OpenAI(
            temperature=0,
            openai_api_key=data.openai_key
        ),
        chain_type="stuff",
        retriever=vector_db.retriever
    )
    return chain({"question": data.question}, return_only_outputs=data.return_only_outputs)
