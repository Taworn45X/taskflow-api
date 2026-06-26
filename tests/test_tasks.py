"""API tests using an isolated in-memory database."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app


@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get_task(client):
    res = client.post("/api/tasks", json={"title": "Buy milk", "priority": "high"})
    assert res.status_code == 201
    task = res.json()
    assert task["title"] == "Buy milk"
    assert task["done"] is False

    got = client.get(f"/api/tasks/{task['id']}")
    assert got.status_code == 200
    assert got.json()["priority"] == "high"


def test_list_and_filter(client):
    client.post("/api/tasks", json={"title": "A", "priority": "low"})
    client.post("/api/tasks", json={"title": "B", "priority": "high"})
    assert len(client.get("/api/tasks").json()) == 2
    assert len(client.get("/api/tasks?priority=high").json()) == 1


def test_update_marks_done(client):
    tid = client.post("/api/tasks", json={"title": "Finish report"}).json()["id"]
    res = client.patch(f"/api/tasks/{tid}", json={"done": True})
    assert res.status_code == 200
    assert res.json()["done"] is True


def test_delete_task(client):
    tid = client.post("/api/tasks", json={"title": "Temp"}).json()["id"]
    assert client.delete(f"/api/tasks/{tid}").status_code == 204
    assert client.get(f"/api/tasks/{tid}").status_code == 404


def test_missing_task_returns_404(client):
    assert client.get("/api/tasks/999").status_code == 404


def test_validation_rejects_empty_title(client):
    assert client.post("/api/tasks", json={"title": ""}).status_code == 422
