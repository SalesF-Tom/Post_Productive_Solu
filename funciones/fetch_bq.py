from google.cloud import bigquery
import os
import json

def fetch_bq_view_data(client):
    query = """
        SELECT distinct
            idform
        FROM 
            `data-warehouse-311917.Productive.tbl_calendar_solicitudes_sf`
        -- WHERE  
        -- lower(sector) = "salesforce";
    """

    try:
        query_job = client.query(query) 
        results = query_job.result()    

        fetched_data = [{"idform": row['idform']} for row in results]

        output_folder = './data'
        os.makedirs(output_folder, exist_ok=True)

        previous_file = os.path.join(output_folder, 'idform_data_previous.json')
        current_file = os.path.join(output_folder, 'idform_data.json')

        if os.path.exists(current_file):
            with open(current_file, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        else:
            current_data = []

        current_ids = {item['idform'] for item in current_data}
        fetched_ids = {item['idform'] for item in fetched_data}

        nuevos = fetched_ids - current_ids

        if nuevos:
            print("Se detectaron nuevos idform:", nuevos)
            
            with open(previous_file, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=4, ensure_ascii=False)

            updated_data = current_data + [{"idform": idform} for idform in nuevos]

            with open(current_file, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)

            # print(f"Datos actualizados. Guardado en {current_file} y {previous_file}")
        else:
            print("No se detectaron nuevos idform.")

        return nuevos
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

def fetch_detailed_data(client, idforms):
    try:
        if not idforms:
            # print("No hay idforms para consultar.")
            return []

        idforms_str = ', '.join([f"'{idform}'" for idform in idforms])

        query = f"""
        SELECT 
          CAST(ppl.person_id AS INT64) AS Person,
          ppl.person AS Name,
          FORMAT_DATE('%Y-%m-%d', s.fecha_ini) AS Start,
          FORMAT_DATE('%Y-%m-%d', s.fecha_fin) AS End_,
          s.licencia_a_solicitar AS Event,
          s.motivo_de_licencia AS Note
        FROM 
          `data-warehouse-311917.Productive.tbl_calendar_solicitudes_sf` s
        JOIN 
          `data-warehouse-311917.Productive.tbl_productive_people` ppl
        ON 
          ppl.email = s.email_solicitante OR s.legajo = ppl.legajo
        WHERE 
          s.idform IN ({idforms_str});
        """

        query_job = client.query(query)
        results = query_job.result()

        data = [dict(row) for row in results]
        return data

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
