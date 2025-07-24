import os
import json
import requests

def reviso_carga(access_token, organization_id):
    all_entitlements = get_licencias(access_token, organization_id)
    
    print(all_entitlements)
    output_folder = './data'
    os.makedirs(output_folder, exist_ok=True)

    path_file = os.path.join(output_folder, 'all_entitlements.json')

    with open(path_file, 'w', encoding='utf-8') as f:
        json.dump(all_entitlements, f, indent=4, ensure_ascii=False)



def get_licencias(access_token, organization_id, filters=None, page_size=100):
    # ?fields[entitlements]=id,account_id,event_id,person_id,start_date,end_date,allocated,used,pending,note,deleted_at,created_at,updated_at,creator_id,updater_id,approval_workflow_id,import_id,deleted_item_id
    base_url = "https://api.productive.io/api/v2/entitlements?fields[entitlements]=external_reference"
    headers = {
        "Accept": "application/vnd.api+json",
        "X-Auth-Token": access_token,
        "X-Organization-Id": organization_id
    }

    params = {}
    if filters:
        params.update(filters)
    params.update({
        "page[size]": page_size,
        "page[number]": 1
    })

    all_entitlements = []
    next_url = base_url

    while next_url:
        resp = requests.get(next_url, headers=headers, params=params)

        if resp.status_code == 401:
            raise RuntimeError(
                "⚠️ 401 Unauthorized: revisa tu X-Auth-Token y X-Organization-Id.\n"
                "   • ¿Token expirado o mal copiado?\n"
                "   • ¿Header mal tipeado (–Id vs –ID)?"
            )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Error {resp.status_code} al obtener entitlements: {resp.text}"
            )

        body = resp.json()
        all_entitlements.extend(body.get("data", []))

        # siguiente página
        links = body.get("links", {})
        next_url = links.get("next")
        params = None

    return all_entitlements