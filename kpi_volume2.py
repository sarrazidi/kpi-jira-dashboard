import sqlite3
import pandas as pd

print("1. Début")

conn = sqlite3.connect("jira_kpi.db")
df = pd.read_sql("SELECT * FROM tickets", conn)
print(f"2. Données chargées : {len(df)} lignes")

df["date_creation"] = pd.to_datetime(df["date_creation"], utc=True)
print("3. Dates converties")

df["jour"] = df["date_creation"].dt.date
print("4. Colonne jour créée")

volume_jour = df.groupby("jour").size().reset_index(name="nombre_tickets")
print("5. Groupby réussi")
print(volume_jour)

conn.close()
print("6. Fin")