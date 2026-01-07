import sys
import os
from fastapi.testclient import TestClient


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)
def test_create_student():
    response = client.post(
        "/students",
        json = {
            "roll_no": 5,
            "name": "Test User",
            "age" : 23,
            "department": "Testing",
            "cgpa": 8.1
        }
    )

    assert response.status_code == 200
    assert response.json()["roll_no"] == 5

def test_get_student_by_roll():
    response = client.get("/students/5")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)