# Utilisez une image de base légère
FROM python:3.8-slim
# Créez et définissez le répertoire de travail
WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY test_e2e.py .

RUN mkdir -p instance
RUN mkdir -p templates


COPY templates/index.html  templates/index.html
#COPY templates/styles.css  templates/styles.css

VOLUME [ "/app/data" ]

# Installez les dépendances
# Exposez le port sur lequel l'application sera accessible
EXPOSE 5000
# Commande pour démarrer l'application Flask
CMD ["python", "main.py"]