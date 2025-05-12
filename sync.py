from jira_fetch import fetch_hp_to_issue

def main():
    print("🔁 מתחיל סנכרון Jira...")
    hp_map = fetch_hp_to_issue()
    if not hp_map:
        print("❌ לא נמצאו ח.פ בטיקטים הפתוחים בפרויקט FCS.")
    else:
        print("✅ מיפוי ח.פ → טיקט:", hp_map)

if __name__ == "__main__":
    main()
