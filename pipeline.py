import os
import subprocess
import logging
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_streamer():
    logging.info("Lancement du streamer...")
    subprocess.run(["python", "streamer.py"], timeout=10)
    logging.info(" Fin streamer.")

def run_prediction():
    logging.info(" Lancement de la prédiction...")
    subprocess.run([
        "curl", "-X", "POST", "http://localhost:5000/forecast",
        "-H", "Content-Type: application/json",
        "-d", "{\"days\": 7}"
    ])
    logging.info(" Fin prédiction.")

if __name__ == "__main__":
    logging.info("===  Pipeline START ===")
    try:
        run_streamer()
        run_prediction()
        logging.info("===  Pipeline END ===")
    except Exception as e:
        logging.error(" Erreur dans le pipeline", exc_info=True)
