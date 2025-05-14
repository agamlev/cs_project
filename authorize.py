from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    print("📡 מתחיל תהליך ההרשאה מול גוגל...")

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

    # הגדרה שעובדת גם ב־Codespaces
    creds = flow.run_local_server(host='localhost', port=8080, authorization_prompt_message='',
                                  success_message='✅ ההתחברות הצליחה! אפשר לחזור לקונסול',
                                  open_browser=False)

    service = build('sheets', 'v4', credentials=creds)
    print("🎉 התחברת בהצלחה ל-Google Sheets")

if __name__ == '__main__':
    main()
