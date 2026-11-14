import pytest

from main import create_app, db


@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.session.remove()
        db.drop_all()


def test_home_page_is_available(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Daily Tasks" in response.data


def test_add_task(client):
    response = client.post("/add", data={"task": "Prepare portfolio"})
    assert response.status_code == 302
    assert b"Prepare portfolio" in client.get("/").data


def test_empty_task_is_rejected(client):
    client.post("/add", data={"task": "   "})
    assert b"Aucune tÃ¢che" in client.get("/").data


def test_task_longer_than_200_characters_is_rejected(client):
    client.post("/add", data={"task": "x" * 201})
    assert b"ne peut pas dÃ©passer 200" in client.get("/").data


def test_delete_task(client):
    client.post("/add", data={"task": "Temporary task"})
    from main import Task
    task = Task.query.first()
    response = client.post(f"/delete/{task.id}")
    assert response.status_code == 302
    assert b"Temporary task" not in client.get("/").data


def test_delete_unknown_task_returns_404(client):
    response = client.post("/delete/999")
    assert response.status_code == 404


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"todo_http_requests_total" in response.data
