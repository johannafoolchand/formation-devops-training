import unittest
from flask_testing import TestCase
from main import app, db, Task  # On importe directement depuis main.py

class YourAppTestCase(TestCase):

def client():
    print("ok ok")      
if __name__ == '__main__':
    unittest.main()