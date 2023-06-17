from pydantic import BaseModel

file_name = "file.pdf"
db_name = "vector_db.pkl"

class OpenAPIBaseModel(BaseModel):
    openai_key: str

class PDFObject(OpenAPIBaseModel):
    file_name: str = file_name
    db_name: str = db_name
