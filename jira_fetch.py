# מייבא ספריות לעבודה עם HTTP, אימות, קבצים וסביבות
import requests
from requests.auth import HTTPBasicAuth
import os
import json

# הגדרות התחברות למערכת Jira
JIRA_DOMAIN = "https://arbox.atlassian.net"         # כתובת המערכת שלך בג'ירה
EMAIL = "agam@arboxapp.com"                         # כתובת המייל שלך בג'ירה
API_TOKEN = os.environ.get("JIRA_API_TOKEN")        # הטוקן שמוגדר כ-Secret בהרצה
HP_FIELDS = ["customfield_10243", "customfield_10244"]  # שמות השדות של הח.פ בטיקטים
MAPPING_FILE = "custom_hp_mapping.json"             # שם קובץ המיפוי שיישמר

# פונקציה שמבצעת בקשה ל-Jira, מחזירה מיפוי של ח.פים לטיקטים
def fetch_hp_to_issue():
    url = f"{JIRA_DOMAIN}/rest/api/3/search"        # כתובת ה-API לחיפוש טיקטים
    params = {
        "jql": 'project = "FCS" AND status != "Done"',  # בקשת JQL: רק טיקטים פעילים בפרויקט FCS
        "fields": ",".join(["key"] + HP_FIELDS),        # נבקש להחזיר רק את המפתח והשדות של הח.פ
        "maxResults": 100                               # מקסימום 100 תוצאות בכל קריאה
    }

    print("שולח בקשה ל-Jira...")                      # לוג לניטור הריצה
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),          # אימות דרך מייל וטוקן
        headers={"Accept": "application/json"}         # פורמט תשובה מבוקש: JSON
    )

    # בדיקה אם הקריאה נכשלה
    if response.status_code != 200:
        print("שגיאה:", response.status_code)
        print(response.text)
        return {}

    # פירוק תגובת ה-JSON והוצאת רשימת הטיקטים
    data = response.json()
    issues = data.get("issues", [])
    print(f"נמצאו {len(issues)} טיקטים.")

    # בניית מיפוי: ח.פ → מפתח טיקט
    hp_to_issue = {}
    for issue in issues:
        key = issue.get("key")
        fields = issue.get("fields", {})
        for field in HP_FIELDS:
            hp = fields.get(field)
            if hp:
                print(f"נמצא ח.פ {hp} בטיקט {key}")
                hp_to_issue[hp] = key  # מוסיף למילון

    return hp_to_issue

# פונקציה ששומרת את המיפוי לקובץ JSON לשימוש בהמשך
def save_hp_mapping(mapping):
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"מיפוי נשמר בקובץ {MAPPING_FILE}")

# קטע שמריץ את הפונקציה אם הקובץ מופעל ישירות
if __name__ == "__main__":
    mapping = fetch_hp_to_issue()        # שליפת המיפוי
    print("המיפוי שנוצר:", mapping)      # הדפסה למסך
    save_hp_mapping(mapping)             # שמירה לקובץ
