import os
import time
from dotenv import load_dotenv
from funciones.bookings import post_bookings
from funciones.bq_client import Get_BQ_client
from funciones.fetch_bq import fetch_bq_view_data, fetch_detailed_data
from funciones.map_events import map_event_to_id

load_dotenv()
# access_token = "71c5be55-e7e8-435c-8ce2-366098478b18"
access_token = os.getenv("ACCESS_TOKEN")
# organization_id = "35584"
organization_id = os.getenv("X_ORGANIZATION_ID")

def main():
    client = Get_BQ_client()

    try:
        # Obtener nuevos IDs
        new_ids = fetch_bq_view_data(client)

        if new_ids:
            upload_data = fetch_detailed_data(client, new_ids)

            mapped_upload_data = map_event_to_id(upload_data)
            print(mapped_upload_data)
            post_bookings(access_token, organization_id, mapped_upload_data)
            
        else:
            print("No se encontraron nuevos ID.")
            time.sleep(10)
    except Exception as e:
        print(f"Error en el proceso principal: {e}")
        time.sleep(10)


if __name__ == "__main__":
    main()
    
