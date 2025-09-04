import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

DB_CONFIG = {
    'dbname': 'sales_4pvm',   #  nom de base
    'user': 'sales_4pvm_user',     #   user
    'password': 'ipdMkrVqQugaI1fvWTmgusk1eAWF6bfq',
    'host': 'dpg-d2sun98dl3ps73ft2rng-a.frankfurt-postgres.render.com',
    'port': 5432      # PostgreSQL utilise "dbname" et non "database"
}


# Connexion DB PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Infos de l’utilisateur à créer
username = "admin"
password = "prediction"

# Hachage du mot de passe
hashed_password = generate_password_hash(password)

# Insertion utilisateur
cursor.execute(
    "INSERT INTO users (username, password) VALUES (%s, %s)",
    (username, hashed_password)
)
conn.commit()

print("Utilisateur créé avec succès 🎉")

cursor.close()
conn.close()
