import sqlite3
import pandas as pd

print("Début du script")

conn = sqlite3.connect("jira_kpi.db")
print("Connexion réussie")

df = pd.read_sql("SELECT * FROM tickets", conn)
print(f"Nombre de lignes récupérées : {len(df)}")
print(df.head())

conn.close()
print("Fin du script")
