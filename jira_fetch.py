import requests
from requests.auth import HTTPBasicAuth
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv  # חדש

# טען משתנים מ-.env
load_dotenv()

# הגדרות Jira
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
HP_FIELDS = ["customfield_10243", "customfield_10244"]
MAPPING_FILE = "custom_hp_mapping.json"

# הגדרות Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SPREADSHEET_NAME = 'Company ID to Jira Mapping'

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
                hp_to_issue[str(hp)] = key

    return hp_to_issue

def save_hp_mapping(mapping):
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"מיפוי נשמר בקובץ {MAPPING_FILE}")

def update_google_sheet(mapping):
    creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    gc = gspread.authorize(creds)

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

# הרצה רגילה
if __name__ == "__main__":
    mapping = fetch_hp_to_issue()
    print("המיפוי שנוצר:", mapping)
    save_hp_mapping(mapping)
    update_google_sheet(mapping)
