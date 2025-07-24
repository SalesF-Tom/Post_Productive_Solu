import requests
from datetime import datetime

def post_licencias(access_token, organization_id, licencias):
    """
    Crea múltiples entitlements (asignaciones de días) en Productive.

    Args:
        access_token (str): Token de autenticación para la API.
        organization_id (str): ID de la organización.
        entitlements (list[dict]): Lista de registros con info de licencia.

    Returns:
        list[dict]: Respuestas de la API.
    """
    url = "https://api.productive.io/api/v2/entitlements"
    headers = {
        "Content-Type": "application/vnd.api+json; charset=utf-8",
        "X-Auth-Token": access_token,
        "X-Organization-Id": organization_id
    }

    responses = []

    for ent in licencias:
        try:
            # Calcular días (inclusive)
            start_date = datetime.strptime(ent["Start"], "%Y-%m-%d")
            end_date = datetime.strptime(ent["End_"], "%Y-%m-%d")
            delta = (end_date - start_date).days + 1
            allocated = delta

            payload = {
                "data": {
                    "type": "entitlements",
                    "attributes": {
                        "event_id": ent["Event"],
                        "person_id": ent["Person"],
                        "start_date": ent["Start"],
                        "end_date": ent["End_"],
                        "allocated": allocated
                    }
                }
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 201:
                print(f"Entitlement creado para {ent['Name']}: {allocated} días.")
            else:
                print(f"Error creando entitlement para {ent['Name']}: {response.status_code} - {response.text}")

            responses.append(response.json())

        except Exception as e:
            print(f"Error en entitlement para {ent.get('Name', 'Desconocido')}: {e}")
            responses.append({"error": str(e)})

    return responses


def buscar_licencias(access_token, organization_id, licencia):
    event_id   = licencia["Event"]
    person_id  = licencia["Person"]
    start_date = licencia["Start"]
    end_date   = licencia["End_"]

    filters = {
        "filter[event_id]":   event_id,
        "filter[person_id]":  person_id,
        "filter[start_date]": start_date,
        "filter[end_date]":   end_date
    }

    matches = get_licencias(access_token, organization_id, filters=filters)

    return matches[0] if matches else None



def get_licencias(access_token, organization_id, filters=None, page_size=100):
    base_url = "https://api.productive.io/api/v2/entitlements"

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