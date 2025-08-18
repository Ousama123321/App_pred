import mysql.connector
import time
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv  # Pour charger les infos sensibles depuis un fichier .env
import os

# Chargement des variables d'environnement
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sale')
}

def get_last_date():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) FROM sales")
        result = cursor.fetchone()[0]
    except mysql.connector.Error as e:
        print(f"[ERREUR] Base de données : {e}")
        result = None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    
    if result:
        return result
    else:
        return datetime.strptime("2017-07-15", "%Y-%m-%d").date()

def insert_new_sale():
    last_date = get_last_date()
    new_date = last_date + timedelta(days=1)
    unit_sales = random.randint(400, 800)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sales (date, unit_sales) VALUES (%s, %s)",
            (new_date, unit_sales)
        )
        conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Vente ajoutée : {new_date} → {unit_sales}")
    except mysql.connector.Error as e:
        print(f"[ERREUR] Insertion échouée : {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def run_streamer():
    """Lance la simulation en continu, utilisable depuis Flask."""
    print("Simulation du flux de ventes MySQL en cours... (Ctrl+C pour arrêter)")
    try:
        while True:
            insert_new_sale()
            time.sleep(5)  # pause entre chaque vente simulée
    except KeyboardInterrupt:
        print("\nSimulation arrêtée.")

# Pour test en standalone
if __name__ == "__main__":
    run_streamer()
