import unittest
from flask_testing import TestCase
from main import app, db, Task  # On importe directement depuis main.py

class YourAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        # Utilisation d'une base de données de test en mémoire
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

if __name__ == '__main__':
    unittest.main()