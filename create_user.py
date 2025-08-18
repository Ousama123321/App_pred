import mysql.connector
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sale')
}

# Connexion DB
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Infos de l’utilisateur à créer
username = "admin"
password = "prediction"

# Hachage du mot de passe
hashed_password = generate_password_hash(password)

# Insertion
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
conn.commit()

print("Utilisateur créé avec succès ")

cursor.close()
conn.close()
