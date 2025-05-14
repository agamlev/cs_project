import gspread
from google.oauth2.service_account import Credentials
from jira_fetch import fetch_hp_to_issue

# טווח ההרשאות הנדרש
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# טעינת ההרשאות מקובץ service_account.json
creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
gc = gspread.authorize(creds)

# פתיחה או יצירה של הגיליון
spreadsheet_name = 'Company ID to Jira Mapping'
try:
    sh = gc.open(spreadsheet_name)
except gspread.SpreadsheetNotFound:
    sh = gc.create(spreadsheet_name)

# שימוש בדף הראשון
worksheet = sh.get_worksheet(0)

# שלב 1: מחיקת התוכן הקיים
worksheet.clear()

# שלב 2: כתיבת כותרות
worksheet.update('A1:B1', [['ח.פ', 'קוד טיקט']])

# שלב 3: שליפת המיפוי והזנה
mapping = fetch_hp_to_issue()
rows = [[str(hp), ticket] for hp, ticket in mapping.items()]
if rows:
    worksheet.update('A2', rows)

print("✅ סנכרון הושלם!")
