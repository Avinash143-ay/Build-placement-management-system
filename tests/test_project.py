import os

import pytest

from placement_system import create_app
from database import BPlusTree


@pytest.fixture
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE": os.path.join(tmp_path, "placement.db"),
        "SECRET_KEY": "test-secret",
    })
    return app.test_client()


def auth_headers(client, email, password):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.get_json()['token']}"}


def test_student_application_workflow(client):
    headers = auth_headers(client, "student@example.com", "student123")
    assert client.get("/api/health").status_code == 200
    assert client.post("/api/jobs/1/applications", headers=headers).status_code == 201
    assert client.post("/api/jobs/1/applications", headers=headers).status_code == 409


def test_role_boundary(client):
    headers = auth_headers(client, "student@example.com", "student123")
    assert client.get("/api/admin/stats", headers=headers).status_code == 403


def test_bplus_tree_search_and_range():
    tree = BPlusTree(order=8)
    for key in range(1000):
        tree.insert(key, str(key))
    assert tree.search(432) == (True, "432")
    assert [key for key, _ in tree.range_query(100, 110)] == list(range(100, 111))