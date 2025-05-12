import requests
from requests.auth import HTTPBasicAuth

JIRA_DOMAIN = "https://arbox.atlassian.net"
EMAIL = "agam@arbox.com"
import os
API_TOKEN = os.environ.get("JIRA_API_TOKEN")

HP_FIELDS = ["customfield_10243", "customfield_10244"]

def fetch_hp_to_issue():
    url = f"{JIRA_DOMAIN}/rest/api/3/search"
    params = {
        "jql": 'project = "FCS" AND status != "Done"',
        "fields": "key," + ",".join(HP_FIELDS),
        "maxResults": 100
    }

    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        print("שגיאה:", response.status_code, response.text)
        return {}

    hp_to_issue = {}
    for issue in response.json()["issues"]:
        key = issue["key"]
        fields = issue["fields"]
        for field in HP_FIELDS:
            hp = fields.get(field)
            if hp:
                hp_to_issue[hp] = key
    return hp_to_issue

# בדיקה מהירה (למטרות פיתוח בלבד)
if __name__ == "__main__":
    mapping = fetch_hp_to_issue()
    print(mapping)
