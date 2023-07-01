import os
import pytest
from fastapi.testclient import TestClient
from backend.app import app as backend_app


backend_client = TestClient(backend_app)


@pytest.fixture
def openai_key():
    return os.environ['OPEN_AI_SECRET_KEY']


@pytest.fixture
def sample_pdf_path():
    return "tests/test_data/sample.pdf"


@pytest.mark.first
def test_dump_pdf(sample_pdf_path):
    with open("tests/test_data/sample.pdf", 'rb') as file:
        pdf_bytes = file.read()

    files = {
        "pdf_bytes": ("sample.pdf", pdf_bytes, "application/pdf")
    }
    response = backend_client.post("/dump_pdf", files=files)
    assert response.status_code == 200
    assert response.json().get("Status") == 200


@pytest.mark.second
def test_create_vec_db(openai_key):
    data = {
        "openai_key": openai_key,
        "file_name": ["sample.pdf"],
        "db_name": "vector_db.pkl"
    }
    response = backend_client.post("/create_vec_db", json=data)
    assert response.status_code == 200
    assert "DB_PATH" in response.json()


@pytest.mark.last
def test_get_answer(openai_key):
    data = {
        "openai_key": openai_key,
        "db_path": "./db/vector_db.pkl",
        "k": 3,
        "question": "test_question",
        "return_only_outputs": True
    }
    response = backend_client.post("/get_answer", json=data)
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()
