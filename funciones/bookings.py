import requests

def post_bookings(access_token, organization_id, bookings):
    """
    Crea múltiples reservas (bookings) para personas en Productive con relaciones especificadas.

    Args:
        access_token (str): Token de autenticación para la API de Productive.
        organization_id (str): ID de la organización en Productive.
        bookings (list[dict]): Lista de diccionarios con los detalles de cada booking.

    Returns:
        list[dict]: Respuestas de la API para cada booking.
    """
    url = "https://api.productive.io/api/v2/bookings"

    headers = {
        "Content-Type": "application/vnd.api+json; charset=utf-8",
        "X-Auth-Token": access_token,
        "X-Organization-Id": organization_id
    }

    responses = []

    for booking in bookings:
        payload = {
            "data": {
                "type": "bookings",
                "attributes": {
                    "person_id": booking["Person"],
                    "started_on": booking["Start"],
                    "ended_on": booking["End_"],
                    "booking_method_id": 2,
                    "event_id": booking.get("Event"),
                    "note": booking.get("Note", ""),
                    "percentage": booking.get("percentage", 100)
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            print(f"Booking creado exitosamente para {booking['Name']}")
        else:
            print(f"Error {response.status_code}: {response.json()}. para {booking['Name']}")

        responses.append(response.json())

    return responses