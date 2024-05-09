from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'secret_key'  # Clé secrète pour les messages flash
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive les avertissements de modification SQLAlchemy
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # Récupère le numéro de page à partir de l'URL
    per_page = 5  # Nombre de tâches à afficher par page
    tasks = Task.query.order_by(desc(Task.id)).paginate(page=page, per_page=per_page)
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_description = request.form['task']
    if not task_description:
        flash('La description de la tâche ne peut pas être vide.', 'error')
    else:
        new_task = Task(description=task_description)
        db.session.add(new_task)
        db.session.commit()
        flash('Tâche ajoutée avec succès.', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.description = request.form['task']
        if not task.description:
            flash('La description de la tâche ne peut pas être vide.', 'error')
        else:
            db.session.commit()
            flash('Tâche modifiée avec succès.', 'success')
            return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task_to_delete = Task.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash('Tâche supprimée avec succès.', 'success')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


