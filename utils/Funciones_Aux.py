# funciones/productive_api.py

import requests

def get_paginated(resource, access_token, organization_id, filters=None, page_size=100):
    """
    GET genérico para recursos JSON:API en Productive (entitlements o bookings).
    """
    base_url = f"https://api.productive.io/api/v2/{resource}"
    headers = {
        "Accept":           "application/vnd.api+json",
        "X-Auth-Token":     access_token,
        "X-Organization-Id": organization_id
    }
    params = {**(filters or {}), "page[size]": page_size, "page[number]": 1}
    all_items, next_url = [], base_url

    while next_url:
        resp = requests.get(next_url, headers=headers, params=params)
        resp.raise_for_status()
        payload = resp.json()
        all_items.extend(payload.get("data", []))
        next_url = payload.get("links", {}).get("next")
        params = None

    return all_items

def get_licencias(access_token, organization_id, filters=None):
    return get_paginated("entitlements", access_token, organization_id, filters)

def get_bookings(access_token, organization_id, filters=None):
    return get_paginated("bookings", access_token, organization_id, filters)


def already_processed(idform, access_token, organization_id):
    """
    Retorna True si el idform ya existe en Entitlements o en Bookings.
    """
    # filtro por external_reference
    f = {"filter[external_reference]": idform}

    if get_licencias(access_token, organization_id, filters=f):
        return True
    if get_bookings(access_token, organization_id, filters=f):
        return True

    return False

def filter_unprocessed(records, access_token, organization_id):
    """
    De una lista de registros (cada uno con key 'idform'), devuelve
    sólo aquellos que no han sido cargados en Productive.
    """
    nuevos = []
    for rec in records:
        idf = rec["idform"]
        if already_processed(idf, access_token, organization_id):
            print(f"🔍 Saltando duplicado: {idf}")
        else:
            nuevos.append(rec)
    return nuevos
