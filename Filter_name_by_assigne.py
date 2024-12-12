import json

# קריאה של קובץ JSON המקורי
with open("invalid_assignees.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# יצירת סט כדי לשמור רק שמות ייחודיים
unique_assignees = set()

# מעבר על כל אובייקט ושמירת השם המופיע ב-AssignedTo
for item in data:
    assigned_to = item.get("AssignedTo")
    if assigned_to:  # רק אם השדה קיים
        unique_assignees.add(assigned_to)

# יצירת רשימה חדשה מהשמות הייחודיים
unique_assignees_list = list(unique_assignees)

# שמירת השמות לקובץ JSON חדש
output_data = {"AssignedTo": unique_assignees_list}

with open("unique_assignees.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("השמות נשמרו בקובץ 'unique_assignees.json'")
