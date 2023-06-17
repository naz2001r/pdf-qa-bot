from fastapi.testclient import TestClient

import sys
sys.path.append('.\\backend\\')
from app import app

client = TestClient(app)


def test_example():
    response = client.get("/example")
    assert response.status_code == 200
