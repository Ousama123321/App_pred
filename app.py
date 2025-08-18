from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
import numpy as np
import joblib
import tensorflow as tf
from datetime import datetime, timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
from functools import wraps
import threading
import streamer
import os

# Charger les variables d’environnement
load_dotenv()

# Configuration sécurisée
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sale')
}

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret_key_placeholder')

# Limiter pour protéger l'app
limiter = Limiter(key_func=get_remote_address, default_limits=["30 per minute"])
limiter.init_app(app)

# Charger modèle et scaler
model = tf.keras.models.load_model("lstm_sales_model.h5")
scaler = joblib.load("scale.save")

# ------------------------------
# Helpers
# ------------------------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ------------------------------
# ROUTES LOGIN/LOGOUT
# ------------------------------
@app.route('/')
def home():
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            # Stocker infos session
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            # Lancer le streamer en arrière-plan
            threading.Thread(target=streamer.run_streamer, daemon=True).start()

            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Nom d’utilisateur ou mot de passe incorrect.")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# ------------------------------
# INDEX PROTÉGÉ
# ------------------------------
@app.route('/index')
@login_required
def index():
    return render_template('index.html', username=session["username"])

# ------------------------------
# PRÉDICTION
# ------------------------------
def get_latest_sales(n_days=30):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, unit_sales FROM sales ORDER BY date DESC LIMIT %s", (n_days,))
    results = cursor.fetchall()
    conn.close()
    results.reverse()
    return [row[1] for row in results]

def get_last_date():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM sales")
    result = cursor.fetchone()[0]
    conn.close()
    return result

def predict_next_days(n_days):
    data = get_latest_sales()
    if len(data) < 30:
        raise ValueError("Pas assez de données pour la prédiction")
    input_seq = scaler.transform(np.array(data).reshape(-1, 1)).reshape(1, len(data), 1)
    predictions = []
    current_input = input_seq
    for _ in range(n_days):
        pred = model.predict(current_input, verbose=0)[0][0]
        predictions.append(pred)
        current_input = np.append(current_input[:, 1:, :], [[[pred]]], axis=1)
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    predictions = [int(round(x[0])) for x in predictions]
    last_date = get_last_date()
    forecast_dates = [(last_date + timedelta(days=i+1)).strftime("%Y-%m-%d") for i in range(n_days)]
    return forecast_dates, predictions

@app.route('/forecast', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
def forecast():
    if not request.is_json:
        return jsonify({"error": "Données JSON requises"}), 400
    data = request.get_json()
    try:
        days = int(data.get('days', 0))
        if days < 1 or days > 30:
            return jsonify({"error": "Le nombre de jours doit être entre 1 et 30"}), 400
    except:
        return jsonify({"error": "Format du paramètre 'days' invalide"}), 400
    try:
        forecast_dates, forecast_values = predict_next_days(days)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"forecast_dates": forecast_dates, "forecast_values": forecast_values})

# ------------------------------
# RUN
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
