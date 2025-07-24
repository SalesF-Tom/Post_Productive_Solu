# utils/Chequeo_Form.py

import os
from dotenv import load_dotenv
from utils.Funciones_Aux import already_processed, get_bookings, get_licencias

load_dotenv()

ACCESS_TOKEN      = os.getenv("ACCESS_TOKEN")
ORGANIZATION_ID   = os.getenv("X_ORGANIZATION_ID")


def chequear_form(idform: str,
                  access_token: str = ACCESS_TOKEN,
                  organization_id: str = ORGANIZATION_ID) -> bool:
    
    if not idform:
        raise ValueError("⚠️ Debes pasar un idform no vacío.")

    # Filtrar por referencia externa
    filtro = {"filter[external_reference]": idform}

    # 1) Compruebo en Entitlements
    ent = get_licencias(access_token, organization_id, filters=filtro)
    if ent:
        return True

    # 2) Compruebo en Bookings
    book = get_bookings(access_token, organization_id, filters=filtro)
    if book:
        return True

    # 3) No está en ninguno
    return False
