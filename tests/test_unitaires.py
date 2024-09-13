import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200  # Vérifie que le statut HTTP est 200 OK
    assert b'Bienvenue sur la page d\'accueil' in response.data  # Vérifie que le texte attendu est dans la réponse
