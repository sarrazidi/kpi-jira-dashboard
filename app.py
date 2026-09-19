from flask import Flask, jsonify, request
import os
import sqlite3
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def get_connection():
    return sqlite3.connect("jira_kpi.db")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return jsonify({"success": True, "token": os.getenv("SECRET_TOKEN")})
    else:
        return jsonify({"success": False, "message": "Identifiants incorrects"}), 401

@app.route("/api/kpi/statut")
def kpi_statut():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM kpi_statut", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/kpi/type")
def kpi_type():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM kpi_type", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/kpi/priorite")
def kpi_priorite():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM kpi_priorite", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/kpi/volume")
def kpi_volume():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM kpi_volume_jour", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/kpi/temps")
def kpi_temps():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM tickets", conn)
    conn.close()

    df["date_creation"] = pd.to_datetime(df["date_creation"], utc=True)
    df["date_resolution"] = pd.to_datetime(df["date_resolution"], utc=True)
    df["temps_resolution_heures"] = (df["date_resolution"] - df["date_creation"]).dt.total_seconds() / 3600

    tickets_resolus = df[df["temps_resolution_heures"].notna()]

    if len(tickets_resolus) == 0:
        return jsonify({
            "temps_moyen_heures": None,
            "nombre_tickets_resolus": 0,
            "sla_respecte_pourcentage": None
        })

    temps_moyen = tickets_resolus["temps_resolution_heures"].mean()

    sla_seuils = {"Highest": 4, "High": 8, "Medium": 48, "Low": 120}

    def sla_respecte(row):
        seuil = sla_seuils.get(row["priorite"], 48)
        return row["temps_resolution_heures"] <= seuil

    tickets_resolus = tickets_resolus.copy()
    tickets_resolus["sla_respecte"] = tickets_resolus.apply(sla_respecte, axis=1)
    taux_respect = (tickets_resolus["sla_respecte"].sum() / len(tickets_resolus)) * 100

    return jsonify({
        "temps_moyen_heures": round(temps_moyen, 1),
        "nombre_tickets_resolus": len(tickets_resolus),
        "sla_respecte_pourcentage": round(taux_respect, 1)
    })

@app.route("/api/tickets")
def get_tickets():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM tickets", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)