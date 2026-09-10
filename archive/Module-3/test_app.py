import os

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE": os.path.join(tmp_path, "placement.db"),
        "SECRET_KEY": "test-secret",
    })
    return app.test_client()


def login(client, email, password):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.get_json()['token']}"}


def test_student_can_apply_once(client):
    headers = login(client, "student@example.com", "student123")
    assert client.post("/api/jobs/1/applications", headers=headers).status_code == 201
    assert client.post("/api/jobs/1/applications", headers=headers).status_code == 409
    assert client.get("/api/applications", headers=headers).get_json()[0]["status"] == "applied"


def test_roles_are_enforced(client):
    student_headers = login(client, "student@example.com", "student123")
    assert client.get("/api/admin/stats", headers=student_headers).status_code == 403
    recruiter_headers = login(client, "recruiter@example.com", "recruiter123")
    response = client.post("/api/recruiter/jobs", headers=recruiter_headers, json={
        "title": "Data Engineer",
        "description": "Build data pipelines.",
        "application_deadline": "2030-12-31",
    })
    assert response.status_code == 201