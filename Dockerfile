# Image de base avec Python 3.11 (compatible avec tes libs)
FROM python:3.11-slim

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential wget git \
    && rm -rf /var/lib/apt/lists/*

# Créer dossier de travail
WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'app
COPY . .

# Exposer le port
EXPOSE 8080

# Lancer Flask avec Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
