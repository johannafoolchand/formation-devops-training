# Utilisez une image de base légère
FROM python:3.8-slim
# Créez et définissez le répertoire de travail
WORKDIR /app
# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt .

COPY main.py .
COPY tests_main.py .
COPY test_e2e.py .

RUN mkdir -p instance
RUN mkdir -p templates

COPY instance/tasks.db  instance/tasks.db
COPY templates/index.html  templates/index.html


# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt
# Exposez le port sur lequel l'application sera accessible
EXPOSE 5000
# Commande pour démarrer l'application Flask
CMD ["python3", "main.py"]