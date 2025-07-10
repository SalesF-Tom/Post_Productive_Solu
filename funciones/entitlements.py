import requests
from datetime import datetime

def post_entitlements(access_token, organization_id, entitlements):
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

    for ent in entitlements:
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
