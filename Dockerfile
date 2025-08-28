# Image de base Python
FROM python:3.10-slim

# Installer dépendances système (nécessaires pour PostgreSQL et TensorFlow)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Créer dossier de travail
WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout ton code dans le conteneur
COPY . .

# Exposer le port (Railway utilisera $PORT automatiquement)
EXPOSE 8080

# Lancer Flask avec gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
