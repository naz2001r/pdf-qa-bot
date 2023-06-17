import sys
sys.path.append('.\\backend\\')
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_example():
    response = client.get("/example")
    assert response.status_code == 200
