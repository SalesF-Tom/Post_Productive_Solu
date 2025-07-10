import os
# from dotenv import load_dotenv
from funciones.bookings import post_bookings
from funciones.entitlements import post_entitlements  # 🚨 Nuevo import
from funciones.bq_client import Get_BQ_client
from funciones.fetch_bq import fetch_bq_view_data, fetch_detailed_data
from funciones.map_events import map_event_to_id


access_token = os.getenv("ACCESS_TOKEN")
organization_id = os.getenv("X_ORGANIZATION_ID")

def main():
    client = Get_BQ_client()

    try:
        # Obtener nuevos IDs
        new_ids = fetch_bq_view_data(client)

        if new_ids:
            upload_data = fetch_detailed_data(client, new_ids)

            mapped_upload_data = map_event_to_id(upload_data)

            # 🚨 Paso nuevo: generar entitlements antes del booking
            post_entitlements(access_token, organization_id, mapped_upload_data)

            # Crear bookings como siempre
            post_bookings(access_token, organization_id, mapped_upload_data)
        else:
            print("No se encontraron nuevos ID.")
    except Exception as e:
        print(f"Error en el proceso principal: {e}")

if __name__ == "__main__":
    main()
