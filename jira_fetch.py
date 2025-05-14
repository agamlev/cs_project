import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

import gspread
from google.oauth2.service_account import Credentials

# טען משתנים מתוך קובץ .env (לעבודה מקומית בלבד – לא מזיק אם זה קיים גם בהרצה ב-GitHub)
load_dotenv()

# משתנים לגישה ל־Jira מה־ENV
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
HP_FIELDS = ["customfield_10243", "customfield_10244"]
MAPPING_FILE = "custom_hp_mapping.json"
SPREADSHEET_NAME = 'Company ID to Jira Mapping'

# הגדרת הרשאות גוגל – הכל מתוך משתני סביבה
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

service_account_info = {
    "type": "service_account",
    "project_id": os.environ.get("GCP_PROJECT_ID"),
    "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("GCP_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
    "client_id": os.environ.get("GCP_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("GCP_CLIENT_CERT")
}

creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
gc = gspread.authorize(creds)

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

    issues = response.json().get("issues", [])
    print(f"נמצאו {len(issues)} טיקטים.")

    hp_to_issue = {}
    for issue in issues:
        key = issue.get("key")
        fields = issue.get("fields", {})
        for field in HP_FIELDS:
            hp = fields.get(field)
            if hp:
                hp_to_issue[str(hp)] = key

    return hp_to_issue

def save_hp_mapping(mapping):
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"מיפוי נשמר בקובץ {MAPPING_FILE}")

def update_google_sheet(mapping):
    try:
        sh = gc.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(SPREADSHEET_NAME)

    worksheet = sh.get_worksheet(0)
    worksheet.clear()
    worksheet.update('A1:B1', [['ח.פ', 'קוד טיקט']])

    rows = [[hp, ticket] for hp, ticket in mapping.items()]
    if rows:
        worksheet.update('A2', rows)

    print("📤 המיפוי עודכן בגוגל שיטס")

# הרצה
if __name__ == "__main__":
    mapping = fetch_hp_to_issue()
    save_hp_mapping(mapping)
    update_google_sheet(mapping)
