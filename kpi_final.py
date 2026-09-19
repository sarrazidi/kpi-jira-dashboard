import sqlite3
import pandas as pd 

conn = sqlite3.connect("jira_kpi.db")
df = pd.read_sql("SELECT * FROM tickets", conn)

# Conversion des dates
df["date_creation"] = pd.to_datetime(df["date_creation"], utc=True)
df["date_resolution"] = pd.to_datetime(df["date_resolution"], utc=True)

# ============================================
# KPI 1-3 : Comptages
# ============================================
kpi_par_statut = df.groupby("statut").size().reset_index(name="nombre_tickets")
kpi_par_type = df.groupby("type").size().reset_index(name="nombre_tickets")
kpi_par_priorite = df.groupby("priorite").size().reset_index(name="nombre_tickets")

# ============================================
# KPI 4-5 : Temps de résolution
# ============================================
df["temps_resolution_heures"] = (df["date_resolution"] - df["date_creation"]).dt.total_seconds() / 3600
tickets_resolus = df[df["temps_resolution_heures"].notna()]
temps_moyen = tickets_resolus["temps_resolution_heures"].mean() if len(tickets_resolus) > 0 else None

# ============================================
# KPI 6 : Respect des SLA
# ============================================
sla_seuils = {"Highest": 4, "High": 8, "Medium": 48, "Low": 120}

def sla_respecte(row):
    if pd.isna(row["temps_resolution_heures"]):
        return None
    seuil = sla_seuils.get(row["priorite"], 48)
    return row["temps_resolution_heures"] <= seuil

df["sla_respecte"] = df.apply(sla_respecte, axis=1)
tickets_juges = df[df["sla_respecte"].notna()]
taux_sla = (tickets_juges["sla_respecte"].sum() / len(tickets_juges) * 100) if len(tickets_juges) > 0 else None

# ============================================
# KPI 7 : Volume par jour
# ============================================
df["jour"] = df["date_creation"].dt.date
kpi_volume_jour = df.groupby("jour").size().reset_index(name="nombre_tickets")

# ============================================
# AFFICHAGE RÉCAPITULATIF
# ============================================
print("=" * 50)
print("RÉCAPITULATIF DE TOUS LES KPI")
print("=" * 50)

print("\n Par statut :")
print(kpi_par_statut)

print("\n Par type :")
print(kpi_par_type)

print("\n Par priorité :")
print(kpi_par_priorite)

print(f"\n Temps moyen de résolution : {temps_moyen:.1f}h" if temps_moyen else "\n📌 Temps moyen : pas de tickets résolus")

print(f"\n Taux de respect SLA : {taux_sla:.1f}%" if taux_sla else "\n📌 SLA : pas de tickets résolus")

print("\n Volume par jour :")
print(kpi_volume_jour)

# ============================================
# SAUVEGARDE DES KPI DANS LA BASE (pour le futur dashboard)
# ============================================
kpi_par_statut.to_sql("kpi_statut", conn, if_exists="replace", index=False)
kpi_par_type.to_sql("kpi_type", conn, if_exists="replace", index=False)
kpi_par_priorite.to_sql("kpi_priorite", conn, if_exists="replace", index=False)
kpi_volume_jour.to_sql("kpi_volume_jour", conn, if_exists="replace", index=False)

print("\n Tous les KPI ont été sauvegardés dans la base de données")

conn.close()