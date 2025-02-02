from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client.from_service_account_json("service-account.json")

DATASET_ID = "university_data"
TABLE_ID = "departments"

def query_bigquery(query: str):
    """Executes a query and returns the result as a list of dictionaries."""
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]
