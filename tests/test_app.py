import pytest

from main import Task, create_app, db


@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as test_client:
            yield test_client
        db.session.remove()
        db.drop_all()


def test_home_page_is_available(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Daily Tasks" in response.get_data(as_text=True)


def test_add_task(client):
    response = client.post("/add", data={"task": "Prepare portfolio"})
    assert response.status_code == 302
    assert "Prepare portfolio" in client.get("/").get_data(as_text=True)


def test_empty_task_is_rejected(client):
    client.post("/add", data={"task": "   "})
    page = client.get("/").get_data(as_text=True)
    assert "La description ne peut pas être vide." in page
    assert Task.query.count() == 0


def test_task_longer_than_200_characters_is_rejected(client):
    client.post("/add", data={"task": "x" * 201})
    page = client.get("/").get_data(as_text=True)
    assert "La tâche ne peut pas dépasser 200 caractères." in page
    assert Task.query.count() == 0


def test_delete_task(client):
    client.post("/add", data={"task": "Temporary task"})
    task = Task.query.first()
    response = client.post(f"/delete/{task.id}")
    assert response.status_code == 302
    assert "Temporary task" not in client.get("/").get_data(as_text=True)


def test_delete_unknown_task_returns_404(client):
    response = client.post("/delete/999")
    assert response.status_code == 404


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"todo_http_requests_total" in response.data
