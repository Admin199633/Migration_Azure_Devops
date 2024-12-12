import requests
import base64
import json

# הנתונים המזהים
personal_access_token = "XXXXXXXXXXXXXXXXXXXXXX"

# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כתובת ה-API של Azure DevOps לקבלת רשימת שדות
base_api_url = "http://192.168.1.132/DefaultCollection/DG-Dev/_apis/wit/fields?api-version=6.0"

# כותרות הבקשה עם טוקן הגישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"
}

# שליחת הבקשה לקבלת שדות
response = requests.get(base_api_url, headers=headers)

# אם הבקשה הצליחה, נבצע ניתוח של התגובה
if response.status_code == 200:
    fields_data = response.json()

    # חיפוש בשדות האם יש שדות מסוג Read-Only
    for field in fields_data.get('value', []):
        if field.get('readOnly', False):  # אם השדה הוא Read-Only
            print(f"שדה Read-Only נמצא: {field['referenceName']} - {field['name']}")
        else:
            print(f"שדה ניתן לעריכה: {field['referenceName']} - {field['name']}")
else:
    print(f"שגיאה בבקשה: {response.status_code} - {response.text}")
