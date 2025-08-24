import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

DB_CONFIG = {
     'dbname': 'sale_jtbx',   # ou ton nom de base
    'user': 'sale_jtbx_user',     # ou ton user
    'password': 'z1FJQ8yElmTcyVi89ILsCcHV9iT7u4xl',
    'host': 'dpg-d2kf5ejipnbc73f26os0-a.frankfurt-postgres.render.com',
    'port': 5432  
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
