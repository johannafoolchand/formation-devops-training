# Utilisez une image de base légère avec Python 3.8
FROM python:3.12-slim

# Créez et définissez le répertoire de travail à /app
WORKDIR /app

# Copiez le fichier des dépendances dans le conteneur
COPY requirements.txt .

# Installez les dépendances Python spécifiées dans requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiez les fichiers de l'application dans le conteneur
COPY main.py .
COPY test_e2e.py .

# Créez les répertoires nécessaires pour les templates et les fichiers statiques
RUN mkdir -p templates
RUN mkdir -p static

# Copiez les fichiers de templates dans le conteneur
COPY templates/index.html templates/index.html
COPY templates/404.html templates/404.html

# Copiez les fichiers CSS dans le répertoire static
COPY templates/styles.css static/styles.css

# Définissez un volume pour les données persistantes
VOLUME [ "/app/data" ]

# Exposez le port 5000 sur lequel l'application Flask sera accessible
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "main.py"]
