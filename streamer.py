import psycopg2
from psycopg2 import sql
import time
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (.env)
load_dotenv()

DB_CONFIG = {
     'dbname': 'sale',   # ou ton nom de base
    'user': 'postgres',     # ou ton user
    'password': 'kahina',
    'host': 'localhost',
    'port': 5432  # PostgreSQL utilise "dbname"
}

def get_connection():
    """Créer une connexion PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

def get_last_date():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) FROM sales;")
        result = cursor.fetchone()[0]
    except Exception as e:
        print(f"[ERREUR] Base de données : {e}")
        result = None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
    if result:
        return result
    else:
        # Date de départ par défaut
        return datetime.strptime("2017-07-15", "%Y-%m-%d").date()

def insert_new_sale():
    last_date = get_last_date()
    new_date = last_date + timedelta(days=1)
    unit_sales = random.randint(400, 800)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sales (date, unit_sales) VALUES (%s, %s);",
            (new_date, unit_sales)
        )
        conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Vente ajoutée : {new_date} → {unit_sales}")
    except Exception as e:
        print(f"[ERREUR] Insertion échouée : {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def run_streamer():
    """Lance la simulation en continu, utilisable depuis Flask ou standalone."""
    print("Simulation du flux de ventes PostgreSQL en cours... (Ctrl+C pour arrêter)")
    try:
        while True:
            insert_new_sale()
            time.sleep(5)  # pause entre chaque vente simulée
    except KeyboardInterrupt:
        print("\nSimulation arrêtée.")

# Pour test en standalone
if __name__ == "__main__":
    run_streamer()
