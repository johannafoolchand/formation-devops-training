"""Small Flask ToDo application with PostgreSQL support and Prometheus metrics."""
import os
import time

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)


REQUEST_COUNT = Counter(
    "todo_http_requests_total",
    "Total HTTP requests handled by the ToDo application",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "todo_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "local-development-key-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///tasks.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.extensions["task_model"] = Task

    @app.before_request
    def start_timer():
        request.start_time = time.perf_counter()

    @app.after_request
    def record_metrics(response):
        if request.endpoint and request.endpoint != "metrics":
            elapsed = time.perf_counter() - getattr(
                request, "start_time", time.perf_counter()
            )
            REQUEST_COUNT.labels(
                request.method, request.endpoint, str(response.status_code)
            ).inc()
            REQUEST_LATENCY.labels(request.method, request.endpoint).observe(elapsed)
        return response

    @app.get("/")
    def index():
        tasks = Task.query.order_by(Task.id.desc()).all()
        return render_template("index.html", tasks=tasks)

    @app.post("/add")
    def add():
        description = request.form.get("task", "").strip()
        if not description:
            flash("La description ne peut pas être vide.", "error")
        elif len(description) > 200:
            flash("La tâche ne peut pas dépasser 200 caractères.", "error")
        else:
            db.session.add(Task(description=description))
            db.session.commit()
            flash("Tâche ajoutée.", "success")
        return redirect(url_for("index"))

    @app.post("/delete/<int:task_id>")
    def delete(task_id):
        task = db.get_or_404(Task, task_id)
        db.session.delete(task)
        db.session.commit()
        flash("Tâche supprimée.", "success")
        return redirect(url_for("index"))

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
