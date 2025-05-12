import requests  # שליחת בקשות HTTP
from requests.auth import HTTPBasicAuth  # לצורך אימות בסיסי עם שם משתמש וסיסמה (או טוקן)
import os  # קריאת משתני סביבה
import json  # עבודה עם קבצי JSON

# הגדרות בסיס למערכת Jira
JIRA_DOMAIN = "https://arbox.atlassian.net"  # דומיין של Jira בענן
EMAIL = "agam@arboxapp.com"  # המשתמש שמבצע את הפנייה ל־Jira
API_TOKEN = os.environ.get("JIRA_API_TOKEN")  # טוקן שמוגדר כמשתנה סביבה ולא נשמר בקוד

# השדות שאנחנו רוצים למשוך מהטיקט: שני שדות של ח.פ מותאמים אישית
HP_FIELDS = ["customfield_10243", "customfield_10244"]

# שם קובץ JSON שבו יישמר המיפוי בין ח.פ למספר טיקט
MAPPING_FILE = "hp_mapping.json"


def fetch_hp_to_issue():
    """
    מבצע קריאה ל-Jira ומחזיר מיפוי בין ערכי ח.פ (customfield) למספרי טיקטים (issue key).
    """

    # כתובת ה-API לחיפוש טיקטים
    url = f"{JIRA_DOMAIN}/rest/api/3/search"

    # פרמטרים לשאילתת JQL:
    # חיפוש כל הטיקטים בפרויקט FCS שאינם בסטטוס "Done", כולל שדות מותאמים אישית + key
    params = {
        "jql": 'project = "FCS" AND status != "Done"',
        "fields": ",".join(["key"] + HP_FIELDS),
        "maxResults": 100  # הגבלה על מספר התוצאות שיחזרו
    }

    # שליחת הבקשה ל-Jira עם אימות ו-Headers
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json"}
    )

    # טיפול בשגיאה מהשרת
    if response.status_code != 200:
        print("שגיאה:", response.status_code)
        print(response.text)  # הדפסת גוף התגובה (לניפוי באגים)
        return {}

    # יצירת מיפוי בין ערכי הח.פ למספר הטיקט המתאים
    hp_to_issue = {}
    for issue in response.json().get("issues", []):
        key = issue.get("key")  # מספר הטיקט (לדוגמה: FCS-28)
        fields = issue.get("fields", {})
        for field in HP_FIELDS:
            hp = fields.get(field)  # ערך הח.פ משדה מותאם אישית
            if hp:
                hp_to_issue[hp] = key  # שמירה במילון: {ח.פ: מספר טיקט}

    return hp_to_issue


# קוד שמורץ אם הקובץ מופעל ישירות (ולא מיובא כמודול)
if __name__ == "__main__":
    # קריאה לפונקציה שמבצעת את השליפה
    mapping = fetch_hp_to_issue()

    # הדפסת המיפוי למסך
    print(mapping)

    # כתיבת המיפוי לקובץ JSON לצורך שימוש בהמשך (למשל לצורך בדיקות במיילים)
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
