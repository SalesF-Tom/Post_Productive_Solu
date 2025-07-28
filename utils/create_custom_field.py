# create_custom_field.py
import os
import requests

# — Variables de entorno —
ACCESS_TOKEN    = os.getenv("ACCESS_TOKEN")
ORGANIZATION_ID = os.getenv("X_ORGANIZATION_ID")

BASE_URL = "https://api.productive.io/api/v2"
HEADERS = {
    "Content-Type": "application/vnd.api+json; charset=utf-8",
    "X-Auth-Token": ACCESS_TOKEN,
    "X-Organization-Id": ORGANIZATION_ID
}

def create_custom_field(field_name="Composite ID", data_type_id=1, customizable_type="entitlements"):
    url = f"{BASE_URL}/custom_fields"
    payload = {
        "data": {
            "type": "custom_fields",
            "attributes": {
                "name": field_name,
                "data_type_id": data_type_id,
                "customidform": customizable_type
            }
        }
    }

    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code == 201:
        field_id = resp.json()["data"]["id"]
        print(f"✔ Campo custom '{field_name}' creado con ID: {field_id}")
        return field_id
    else:
        print(f"✘ Error {resp.status_code} al crear campo custom:\n{resp.text}")
        resp.raise_for_status()

if __name__ == "__main__":
    create_custom_field()
