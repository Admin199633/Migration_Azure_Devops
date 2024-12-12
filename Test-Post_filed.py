import requests
import json
import base64

# נתונים מזהים (מילוי פרטים מתאימים)
personal_access_token = "XXXXXXXXXXXXXXXXXXXXXX"

# כתובת בסיסית ל-API של Azure DevOps
base_api_url = "http://192.168.1.132/DefaultCollection/DG-Dev/_apis/wit/workitems"

# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות בקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}

# קריאה לקובץ JSON שמכיל את נתוני ה-Work Items
with open("all_work_items_fields.json", "r", encoding="utf-8") as file:
    work_items = json.load(file)

# פונקציה לעדכון Work Item
def update_work_item(item):
    # שליפת מזהה ה-Work Item
    work_item_id = item.get("ID")

    # עדכון כתובת ה-API עם מזהה ה-Work Item
    api_url = f"{base_api_url}/{work_item_id}?api-version=6.0"

    patch_data = []

    # בדיקה אם השדה AcceptanceCriteria קיים תחת Fields
    fields = item.get("Fields", {})
    acceptance_criteria = fields.get("Microsoft.VSTS.Common.AcceptanceCriteria")
    System_Info = fields.get("Microsoft.VSTS.TCM.SystemInfo")


    if acceptance_criteria:
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
            "value": acceptance_criteria
        })

    patch_data.append(    {
        "op": "replace",  # או "add" אם השדה ריק
        "path": "/fields/Microsoft.VSTS.TCM.SystemInfo",
        "value": System_Info
    }
    )



    # בדיקה אם יש נתונים לעדכון
    if not patch_data:
        print(f"No updates for Work Item {work_item_id}. Skipping.")
        return

    # שליחת הבקשה לעדכון ה-Work Item
    response = requests.patch(api_url, headers=headers, json=patch_data)

    if response.status_code == 200:
        print(f"Work Item {work_item_id} has been updated successfully.")
    else:
        print(
            f"Failed to update Work Item {work_item_id}. Status code: {response.status_code}, Message: {response.text}")

# עדכון כל ה-Work Items
for item in work_items:
    update_work_item(item)
