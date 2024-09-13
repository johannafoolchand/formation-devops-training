# Utilisez une image de base légère
FROM python:3.8-slim
# Créez et définissez le répertoire de travail
WORKDIR /app
# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt /app
COPY main.py /app

RUN mkdir -p /app/instance
RUN mkdir -p /app/templates

COPY instance/tasks.db  /app/instance/
COPY templates/index.html  /app/templates/
RUN chmod -R 777 /app/instance

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt
# Exposez le port sur lequel l'application sera accessible
EXPOSE 5000
# Commande pour démarrer l'application Flask
CMD ["python3", "main.py"]