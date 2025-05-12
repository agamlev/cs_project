import json
import os

MAPPING_FILE = "hp_mapping.json"

def load_hp_mapping():
    """טוען את מיפוי הח.פ מתוך קובץ JSON אם קיים"""
    if not os.path.exists(MAPPING_FILE):
        print("לא נמצא קובץ מיפוי:", MAPPING_FILE)
        return {}

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        print("מיפוי נטען בהצלחה:\n")
        for hp, issue_key in mapping.items():
            print(f"ח.פ: {hp} → טיקט: {issue_key}")
        return mapping

# הרצה לבדיקה מקומית
if __name__ == "__main__":
    mapping = load_hp_mapping()
