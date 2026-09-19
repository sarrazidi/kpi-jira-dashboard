import sqlite3
import pandas as pd

conn = sqlite3.connect("jira_kpi.db")

df = pd.read_sql("SELECT * FROM tickets", conn)

df["date_creation"] = pd.to_datetime(df["date_creation"], utc=True)

# ============================================
# KPI 7 : Volume de tickets par jour
# ============================================
df["jour"] = df["date_creation"].dt.date

print("=" * 50)
print("KPI 7 — Volume de tickets par jour")
print("=" * 50)
volume_jour = df.groupby("jour").size().reset_index(name="nombre_tickets")
print(volume_jour)

# ============================================
# KPI 8 : Volume de tickets par semaine
# ============================================
df["semaine"] = df["date_creation"].dt.to_period("W").astype(str)

print("\n" + "=" * 50)
print("KPI 8 — Volume de tickets par semaine")
print("=" * 50)
volume_semaine = df.groupby("semaine").size().reset_index(name="nombre_tickets")
print(volume_semaine)

conn.close()