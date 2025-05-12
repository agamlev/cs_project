import json
import os

MAPPING_FILE = "hp_mapping.json"

# קריאת המיפוי שהתקבל מקובץ ה־JSON
def load_hp_mapping():
    if not os.path.exists(MAPPING_FILE):
        print("לא נמצא קובץ המיפוי.")
        return {}
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# פונקציה להדפסת המיפוי
def process_mapping():
    hp_to_issue = load_hp_mapping()
    if hp_to_issue:
        print("מיפוי התקבל:", hp_to_issue)
    else:
        print("לא התקבל מיפוי.")
    
# הרצה לבדיקה מקומית
if __name__ == "__main__":
    process_mapping()
