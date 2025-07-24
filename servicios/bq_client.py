import os
from google.cloud import bigquery

def Get_BQ_client():
    credentials_path = './credenciales/data-warehouse-311917-73a0792225c7.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    os.environ['GOOGLE_CLOUD_DISABLE_GRPC'] = 'True'
    project_id="data-warehouse-311917"

    clientBQ = bigquery.Client(project=project_id)

    return clientBQ