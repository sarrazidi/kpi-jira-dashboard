import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os 
import pandas as pd 
import sqlite3

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

url = f"{JIRA_URL}/rest/api/3/search/jql"
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {"Accept": "application/json"}
params = {
    "jql": "project = HELP",
    "maxResults": 50,
    "fields": "summary,status,issuetype,priority,created,assignee,resolutiondate"
}

response = requests.get(url, headers=headers, params=params, auth=auth)

if response.status_code != 200:
    print(f" Erreur lors de l'extraction : {response.status_code}")
    print(response.text)
    exit()

data = response.json()
issues = data["issues"]
print(f" {len(issues)} tickets récupérés depuis Jira")

tickets_list = []

for issue in issues:
    fields = issue["fields"]
    ticket = {
        "cle": issue["key"],
        "resume": fields["summary"],
        "type": fields["issuetype"]["name"],
        "statut": fields["status"]["name"],
        "priorite": fields["priority"]["name"] if fields.get("priority") else "Non défini",
        "date_creation": fields["created"],
        "date_resolution": fields["resolutiondate"] if fields.get("resolutiondate") else None,
        "assigne": fields["assignee"]["displayName"] if fields.get("assignee") else "Non assigné"
    }
    tickets_list.append(ticket)

df = pd.DataFrame(tickets_list)

print("\n Aperçu du tableau pandas :\n")
print(df.head())
print(f"\nNombre total de lignes : {len(df)}")
print(f"Colonnes : {list(df.columns)}")

conn = sqlite3.connect("jira_kpi.db")
df.to_sql("tickets", conn, if_exists="replace", index=False)
print("\n Données insérées dans la base de données 'jira_kpi.db', table 'tickets'")

verification = pd.read_sql("SELECT * FROM tickets", conn)
print(f"\n Vérification : {len(verification)} lignes trouvées dans la base de données")
print(verification.head())

conn.close()