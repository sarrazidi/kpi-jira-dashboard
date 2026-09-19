import sqlite3
import pandas as pd

conn = sqlite3.connect("jira_kpi.db")

df = pd.read_sql("SELECT * FROM tickets", conn)

# Convertir les dates en format standardisé (utc=True corrige le problème de fuseau horaire)
df["date_creation"] = pd.to_datetime(df["date_creation"], utc=True)
df["date_resolution"] = pd.to_datetime(df["date_resolution"], utc=True)

# KPI 4 : Temps de résolution par ticket (en heures)
df["temps_resolution_heures"] = (df["date_resolution"] - df["date_creation"]).dt.total_seconds() / 3600

print("=" * 50)
print("KPI 4 — Temps de résolution par ticket (en heures)")
print("=" * 50)
print(df[["cle", "statut", "date_creation", "date_resolution", "temps_resolution_heures"]])

# KPI 5 : Temps moyen de résolution
tickets_resolus = df[df["temps_resolution_heures"].notna()]

if len(tickets_resolus) > 0:
    temps_moyen = tickets_resolus["temps_resolution_heures"].mean()
    print("\n" + "=" * 50)
    print("KPI 5 — Temps moyen de résolution")
    print("=" * 50)
    print(f"Nombre de tickets résolus : {len(tickets_resolus)}")
    print(f"Temps moyen de résolution : {temps_moyen:.1f} heures ({temps_moyen/24:.1f} jours)")
else:
    print("\n Aucun ticket résolu pour l'instant, impossible de calculer le temps moyen.")

# KPI 6 : Respect des SLA
sla_seuils = {
    "Highest": 4,
    "High": 8,
    "Medium": 48,
    "Low": 120
}

def sla_respecte(row):
    if pd.isna(row["temps_resolution_heures"]):
        return None
    seuil = sla_seuils.get(row["priorite"], 48)
    return row["temps_resolution_heures"] <= seuil

df["sla_respecte"] = df.apply(sla_respecte, axis=1)

print("\n" + "=" * 50)
print("KPI 6 — Respect des SLA")
print("=" * 50)
tickets_juges = df[df["sla_respecte"].notna()]
if len(tickets_juges) > 0:
    taux_respect = (tickets_juges["sla_respecte"].sum() / len(tickets_juges)) * 100
    print(f"Tickets évalués : {len(tickets_juges)}")
    print(f"SLA respecté : {tickets_juges['sla_respecte'].sum()} / {len(tickets_juges)} ({taux_respect:.1f}%)")
else:
    print(" Aucun ticket résolu pour évaluer le respect des SLA.")

conn.close()