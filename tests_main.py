import unittest
from flask_testing import TestCase
from main import app, db, Task  # On importe directement depuis main.py

class YourAppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        # Utilisation d'une base de données de test en mémoire
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db''
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        # Initialisation des données de test si nécessaire

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_task(self):
        response = self.client.post('/add', data={'task': 'Nouvelle tâche de test'})
        self.assertEqual(response.status_code, 302)  # Vérification de la redirection

        # Assurez-vous que la tâche a été ajoutée à la base de données
        task = Task.query.first()
        self.assertIsNotNone(task)
        self.assertEqual(task.description, 'Nouvelle tâche de test')

    def test_delete_task(self):
        # Ajout d'une tâche pour pouvoir la supprimer
        test_task = Task(description='Tâche à supprimer')
        db.session.add(test_task)
        db.session.commit()

        response = self.client.post(f'/delete/{test_task.id}')
        self.assertEqual(response.status_code, 302)  # Vérification de la redirection

        # Assurez-vous que la tâche a été supprimée de la base de données
        deleted_task = Task.query.get(test_task.id)
        self.assertIsNone(deleted_task)

    def test_task_list_display(self):
        # Ajout de tâches de test à la base de données
        task1 = Task(description='Tâche 1')
        task2 = Task(description='Tâche 2')
        db.session.add_all([task1, task2])
        db.session.commit()

        response = self.client.get('/')
        self.assert200(response)  # Vérification de l'affichage de la page

        # Vérifiez que les tâches sont affichées sur la page
        self.assertIn('Tâche 1', response.data.decode())
        self.assertIn('Tâche 2', response.data.decode())

if __name__ == '__main__':
    unittest.main()