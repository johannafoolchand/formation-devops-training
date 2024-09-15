from flask import Flask, render_template, request, redirect, url_for, flash
from prometheus_client import Counter, Histogram, generate_latest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
import time
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configuration du chemin relatif pour la base de données PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/mydatabase'
app.config['SECRET_KEY'] = 'secret_key'  # Clé secrète pour les messages flash
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Création de l'objet SQLAlchemy
db = SQLAlchemy(app)

# Définition du modèle Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)


# Compteur et histogramme pour les métriques Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total number of HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request latency',
    ['method', 'endpoint']
)

# Route pour exposer les métriques Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest()

# Fonction exécutée avant chaque requête
@app.before_request
def before_request():
    request._start_time = time.time()

# Fonction exécutée après chaque requête pour enregistrer les métriques
@app.after_request
def after_request(response):
    if request.endpoint in ['index', 'add', 'delete']:
        request_end_time = time.time()
        request_latency = request_end_time - request._start_time
        path = request.path
        REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(request_latency)
    return response

# Route pour afficher les tâches
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Route pour ajouter une nouvelle tâche
@app.route('/add', methods=['POST'])
def add():
    task_description =request.form.get("task") 
    if task_description:
        new_task = Task(description=task_description)
        db.session.add(new_task)
        db.session.commit()
        flash('Tâche ajoutée avec succès.', 'success')
    else:
        flash('La description de la tâche ne peut pas être vide.', 'error')
    return redirect(url_for('index'))


# Route pour supprimer une tâche
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash('Tâche supprimée avec succès.', 'success')
    return redirect(url_for('index'))

# Route pour gérer les erreurs 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Démarrage de l'application Flask
if __name__ == '__main__':

    with app.app_context():
        db.create_all()  # Cette commande crée la base de données et la table Task si elles n'existent pas déjà
    app.run(host='0.0.0.0', port=5000, debug=True)

