import json
import os
import requests
from requests.auth import HTTPBasicAuth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# הגדרות Jira
JIRA_DOMAIN = "https://arbox.atlassian.net"
EMAIL = "agam@arboxapp.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")

HP_FIELDS = ["customfield_10243", "customfield_10244"]
MAPPING_FILE = "hp_mapping.json"  # שם הקובץ שבו נשמור את המיפוי

def fetch_hp_to_issue():
    """שולף את המידע מ-Jira ומעדכן את קובץ ה-JSON"""
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

    # שמירה לקובץ JSON
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(hp_to_issue, f, ensure_ascii=False, indent=2)
    print(f"מיפוי נשמר בקובץ {MAPPING_FILE}")

    return hp_to_issue

def load_hp_mapping():
    """טוען את המיפוי מקובץ ה-JSON"""
    if not os.path.exists(MAPPING_FILE):
        print(f"קובץ {MAPPING_FILE} לא קיים")
        return {}

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        print("המיפוי נטען:", mapping)
        return mapping

def read_unread_emails():
    """קורא את המיילים הלא נקראים ב-Gmail"""
    creds = Credentials.from_authorized_user_file("gmail_token.json")
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q="is:unread").execute()
    messages = results.get('messages', [])

    content = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        parts = msg_data['payload'].get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data')
                if data:
                    text = base64.urlsafe_b64decode(data.encode()).decode()
                    content.append(text)
    return content

def post_comment_to_jira(issue_key, content):
    """מוסיף תגובה לטיקט ב-Jira"""
    url = f"{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}/comment"
    body = {"body": content}
    response = requests.post(
        url,
        data=json.dumps(body),
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )
    if response.status_code != 201:
        print(f"שגיאה בהוספת תגובה לטיקט {issue_key}: {response.text}")

def main():
    # שולף ומעדכן את קובץ ה-JSON לפני כל הריצה
    fetch_hp_to_issue()
    hp_to_issue = load_hp_mapping()
    email_texts = read_unread_emails()

    for body in email_texts:
        for hp, issue_key in hp_to_issue.items():
            if hp in body:
                print(f"נמצא ח.פ {hp} בהודעה – נוסיף תגובה לטיקט {issue_key}")
                post_comment_to_jira(issue_key, f"התקבלה התכתבות רלוונטית באימייל הכוללת את ח.פ {hp}")

if __name__ == "__main__":
    main()
