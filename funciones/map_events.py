def map_event_to_id(data):
    dic_events_id = {
        "Día de estudio 📚": 130037,
        "Ausencia con aviso 📲(Trámite personal, turno médico, etc.)": 109454,
        "Otras ausencias (Ej: matrimonio, paternidad, fallecimiento, trámites judiciales, etc.)": 141046, #cambia
        "Licencia médica 🏥(Adjuntar certificado de reposo)": 141042, #cambia
        "Licencia por vacaciones🏝️": 109452,
        "Licencia sin goce": 109452,
        "Día de cumpleaños 🎂": 116814
    }
    try:
        for record in data:
            event = record.get("Event")
            if event in dic_events_id:
                record["Event"] = dic_events_id[event]
            else:
                print(f"Evento no mapeado: {event}")
        return data
    except Exception as e:
        print(f"Error al mapear eventos: {e}")
        return []
