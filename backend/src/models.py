from pydantic import BaseModel

try:
    from src.constants import file_name, db_name
except ImportError:
    from backend.src.constants import file_name, db_name


class OpenAPIBaseModel(BaseModel):
    """
    Base class for OpenAPI models.
    """

    openai_key: str


class PDFObject(OpenAPIBaseModel):
    """
    Represents a PDF object with associated file name and database name.
    """

    file_names: list[str] = [file_name]
    db_name: str = db_name


class QueryObject(OpenAPIBaseModel):
    """
    Represents a query object used for querying a database.
    """

    db_path: str
    k: int = 3
    question: str
    return_only_outputs: bool = True
