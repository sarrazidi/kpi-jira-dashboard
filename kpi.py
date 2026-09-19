import sqlite3
import pandas as pd

# Connexion à la base de données déjà créée
conn = sqlite3.connect("jira_kpi.db")

# ============================================
# KPI 1 : Nombre de tickets par statut
# ============================================
print("=" * 50)
print("KPI 1 — Nombre de tickets par statut")
print("=" * 50)

query1 = """
SELECT statut, COUNT(*) as nombre_tickets
FROM tickets
GROUP BY statut
ORDER BY nombre_tickets DESC
"""
df1 = pd.read_sql(query1, conn)
print(df1)

# ============================================
# KPI 2 : Nombre de tickets par type
# ============================================
print("\n" + "=" * 50)
print("KPI 2 — Nombre de tickets par type")
print("=" * 50)

query2 = """
SELECT type, COUNT(*) as nombre_tickets
FROM tickets
GROUP BY type
ORDER BY nombre_tickets DESC
"""
df2 = pd.read_sql(query2, conn)
print(df2)

# ============================================
# KPI 3 : Répartition par priorité
# ============================================
print("\n" + "=" * 50)
print("KPI 3 — Répartition par priorité")
print("=" * 50)

query3 = """
SELECT priorite, COUNT(*) as nombre_tickets
FROM tickets
GROUP BY priorite
ORDER BY nombre_tickets DESC
"""
df3 = pd.read_sql(query3, conn)
print(df3)

conn.close()