# ... כל הייבוא נשאר כמו שהיה

MAPPING_FILE = "custom_hp_mapping.json"  # ← עודכן לשם הנכון

# ... שאר הקוד לא משתנה

def load_hp_mapping():
    if not os.path.exists(MAPPING_FILE):
        return {}
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
