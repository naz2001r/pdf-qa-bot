from pydantic import BaseModel
try:
    from src.constants import file_name, db_name
except:
    from backend.src.constants import file_name, db_name

class OpenAPIBaseModel(BaseModel):
    openai_key: str

class PDFObject(OpenAPIBaseModel):
    file_name: str = file_name
    db_name: str = db_name

class QueryObject(OpenAPIBaseModel):
    db_path: str
    k: int = 3 
    question: str
    return_only_outputs: bool = True