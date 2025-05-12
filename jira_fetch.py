import requests
from requests.auth import HTTPBasicAuth
import os
import json

# הגדרות חיבור ל-Jira
JIRA_DOMAIN = "https://arbox.atlassian.net"
EMAIL = "agam@arboxapp.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")

# שדות ח.פ לשאיבה
HP_FIELDS = ["customfield_10243", "customfield_10244"]
MAPPING_FILE = "hp_mapping.json"  # שם הקובץ המקומי שבו נשמור את המיפוי


def fetch_hp_to_issue():
    """מבצע שאילתת JQL ומחזיר מיפוי של ח.פים למספרי טיקטים"""
    url = f"{JIRA_DOMAIN}/rest/api/3/search"
    params = {
        "jql": 'project = "FCS" AND status != "Done"',
        "fields": ",".join(["key"] + HP_FIELDS),
        "maxResults": 100
    }

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

    hp_to_issue = {}
    for issue in response.json().get("issues", []):
        key = issue.get("key")
        fields = issue.get("fields", {})
        for field in HP_FIELDS:
            hp = fields.get(field)
            if hp:
                hp_to_issue[hp] = key
    return hp_to_issue


def save_hp_mapping(mapping):
    """שומר את המיפוי לקובץ JSON ומדפיס את תוכנו"""
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"מיפוי נשמר בקובץ {MAPPING_FILE}")

    # הדפסת תוכן הקובץ שנשמר
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        print("תוכן הקובץ:")
        print(f.read())


# הרצה לבדיקה מקומית
if __name__ == "__main__":
    mapping = fetch_hp_to_issue()
    print("מיפוי שהתקבל:", mapping)
    save_hp_mapping(mapping)
