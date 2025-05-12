import requests
from requests.auth import HTTPBasicAuth
import os
import json

# הגדרות Jira
JIRA_DOMAIN = "https://arbox.atlassian.net"
EMAIL = "agam@arboxapp.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")
HP_FIELDS = ["customfield_10243", "customfield_10244"]
MAPPING_FILE = "custom_hp_mapping.json"

def fetch_hp_to_issue():
    url = f"{JIRA_DOMAIN}/rest/api/3/search"
    params = {
        "jql": 'project = "FCS" AND status != "Done"',
        "fields": ",".join(["key"] + HP_FIELDS),
        "maxResults": 100
    }

    print("שולח בקשה ל-Jira...")
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        print("שגיאה:", response.status_code)
        print(response.text)
        return {}

    data = response.json()
    issues = data.get("issues", [])
    print(f"נמצאו {len(issues)} טיקטים.")

    hp_to_issue = {}
    for issue in issues:
        key = issue.get("key")
        fields = issue.get("fields", {})
        for field in HP_FIELDS:
            hp = fields.get(field)
            if hp:
                print(f"נמצא ח.פ {hp} בטיקט {key}")
                hp_to_issue[hp] = key

    return hp_to_issue

def save_hp_mapping(mapping):
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"מיפוי נשמר בקובץ {MAPPING_FILE}")

# הרצה מקומית או בגיטהאב
if __name__ == "__main__":
    mapping = fetch_hp_to_issue()
    print("המיפוי שנוצר:", mapping)
    save_hp_mapping(mapping)
