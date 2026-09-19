
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

url = f"{JIRA_URL}/rest/api/3/search/jql"

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json"
}

params = {
    "jql": "project = HELP",
    "maxResults": 50,
    "fields": "summary,status,issuetype,priority,created,assignee"
}

response = requests.get(url, headers=headers, params=params, auth=auth)

print("STATUS CODE:", response.status_code)

if response.status_code == 200:
    data = response.json()
    issues = data["issues"]
    print(f" Connexion réussie ! Nombre de tickets récupérés : {len(issues)}")
    print("\nAperçu des tickets :\n")
    for issue in issues:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        status = issue["fields"]["status"]["name"]
        issue_type = issue["fields"]["issuetype"]["name"]
        priority = issue["fields"]["priority"]["name"] if issue["fields"].get("priority") else "Non défini"
        created = issue["fields"]["created"]
        assignee = issue["fields"]["assignee"]["displayName"] if issue["fields"].get("assignee") else "Non assigné"
        print(f"- {key} | {summary} | Type: {issue_type} | Statut: {status} | Priorité: {priority} | Créé: {created} | Assigné: {assignee}")
else:
    print(f" Erreur : {response.status_code}")
    print(response.text)