import pytest
import requests
import re
from main import app, db, Task

# Définir une fixture pytest pour l'URL de base de l'application
@pytest.fixture
def base_url():
    return 'http://127.0.0.1:5000'  # Mettez l'URL de votre application Flask si différent

# Définir une fixture pytest pour configurer l'application Flask pour les tests
@pytest.fixture
def setup_app(base_url):
    yield       

# Fonction pour extraire les IDs des tâches à partir du contenu de la réponse
def extract_task_ids(response_content):
    # Define a regular expression pattern to match task IDs in the href="/delete/4" format
    pattern = b'/delete/(\d+)'
    # Use re.findall to extract all task IDs from the response content
    task_ids = re.findall(pattern, response_content)
    # Convertion des tasks_ids de string a int
    return list(map(int, task_ids))

# Test d'ajout et de suppression de tâches
def test_add_and_delete_task(base_url, setup_app):
    # Test d'ajout d'une tâche
    response = requests.post(f'{base_url}/add', data={'task': 'Nouvelle tache'})

    # Vérifier que la tâche a été ajoutée
    response = requests.get(f'{base_url}')
    assert response.status_code == 200  # Assurez-vous que la page d'accueil est accessible
    assert b'Nouvelle tache' in response.content  # Vérifier que la tâche est affichée sur la page d'accueil

    # Test de suppression de toutes les tâches
    task_ids = extract_task_ids(response.content)
    for task_id in task_ids:
        # Test de suppression de la tâche
        response = requests.get(f'{base_url}/delete/{task_id}')
        assert response.status_code == 200  # Assurez-vous que la redirection après la suppression est réussie

    # Vérifier que toutes les tâches ont été supprimées
    response = requests.get(f'{base_url}')
    assert response.status_code == 200  # Assurez-vous que la page d'accueil est accessible
    assert b'Nouvelle tache' not in response.content  # Vérifier que les tâches ne sont plus présentes

# Test de la page d'accueil
def test_index_page(base_url, setup_app):
    # Test de la page d'index
    response = requests.get(f'{base_url}/')
    assert response.status_code == 200  # Assurez-vous que la page d'accueil est accessible

    # Vous pouvez également vérifier le contenu de la réponse pour vous assurer que vos données sont correctement rendues
    assert b'ToDo List' in response.content  # Vérifiez qu'une chaîne attendue est présente dans le contenu
