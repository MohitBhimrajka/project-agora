import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str):
    """Creates a BigQuery dataset if it does not already exist."""
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset '{dataset_id}' already exists.")
    except NotFound:
        print(f"Dataset '{dataset_id}' not found. Creating...")
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset '{dataset.project}.{dataset.dataset_id}'.")

def load_csv_to_bigquery(client: bigquery.Client, dataset_name: str, table_name: str, csv_filepath: str):
    """Loads a CSV file into a BigQuery table, overwriting if it exists."""
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Overwrite the table
    )

    with open(csv_filepath, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Wait for the job to complete
    print(f"Loaded {job.output_rows} rows into '{dataset_name}.{table_name}'.")

def setup():
    """Main function to load the mock database into BigQuery."""
    project_id = os.getenv("BQ_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID")
    
    if not project_id or not dataset_id:
        raise ValueError("BQ_PROJECT_ID and BQ_DATASET_ID environment variables must be set.")
        
    full_dataset_id = f"{project_id}.{dataset_id}"
    table_name = "resolved_tickets"
    csv_filepath = "data/resolved_tickets.csv"

    if not os.path.exists(csv_filepath):
        print(f"Error: Mock database file not found at '{csv_filepath}'.")
        print("Please run 'python scripts/create_mock_db.py' first.")
        return

    bq_client = bigquery.Client(project=project_id)
    create_dataset_if_not_exists(bq_client, full_dataset_id)
    load_csv_to_bigquery(bq_client, dataset_id, table_name, csv_filepath)
    print("✅ BigQuery setup complete.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    setup()