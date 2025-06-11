# FILE: scripts/setup_bigquery.py

import os
import json
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str):
    """Creates a BigQuery dataset if it does not already exist."""
    try:
        client.get_dataset(dataset_id)
        print(f"INFO: Dataset '{dataset_id}' already exists.")
    except NotFound:
        print(f"INFO: Dataset '{dataset_id}' not found. Creating...")
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"INFO: Created dataset '{dataset.project}.{dataset.dataset_id}'.")

def load_csv_to_bigquery(client: bigquery.Client, dataset_name: str, table_name: str, csv_filepath: str):
    """Loads a CSV file with an embedding column into a BigQuery table, overwriting if it exists."""
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    # Explicitly define the schema to handle the vector embedding
    schema = [
        bigquery.SchemaField("ticket_id", "STRING"),
        bigquery.SchemaField("customer_id", "STRING"),
        bigquery.SchemaField("request", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("suggested_solution", "STRING"),
        bigquery.SchemaField("request_embedding", "FLOAT64", mode="REPEATED"), # Important: this defines the vector
    ]

    # --- THIS IS THE FIX ---
    # Create a new job_config specifically for loading JSON data.
    # It only needs the schema and the write disposition.
    json_job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Overwrite the table
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, # Specify the source format
    )
    # -----------------------
    
    print(f"INFO: Preparing to load data into '{dataset_name}.{table_name}'...")
    
    # We will convert the CSV to a newline-delimited JSON file in memory
    rows_to_load_as_json_strings = []
    with open(csv_filepath, 'r', encoding='utf-8') as source_file:
        import csv
        reader = csv.reader(source_file)
        header = next(reader) # skip header
        
        for row in reader:
            row_dict = dict(zip(header, row))
            try:
                # Convert the string representation of a list into an actual list of floats
                row_dict['request_embedding'] = json.loads(row_dict['request_embedding'])
                # Convert the entire dictionary to a JSON string for this row
                rows_to_load_as_json_strings.append(json.dumps(row_dict))
            except (json.JSONDecodeError, TypeError) as e:
                print(f"WARN: Could not parse embedding for ticket {row_dict.get('ticket_id')}. Skipping. Error: {e}")

    if not rows_to_load_as_json_strings:
        print("ERROR: No rows were prepared for loading. Check the CSV format and content.")
        return
        
    # Join the JSON strings with newlines to create the in-memory file content
    in_memory_json_file = "\n".join(rows_to_load_as_json_strings).encode('utf-8')
    
    from io import BytesIO
    
    # Load the table from the in-memory BytesIO object
    job = client.load_table_from_file(BytesIO(in_memory_json_file), table_ref, job_config=json_job_config)

    job.result()  # Wait for the job to complete
    print(f"INFO: Loaded {job.output_rows} rows into '{dataset_name}.{table_name}'.")

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
        print(f"ERROR: Mock database file not found at '{csv_filepath}'.")
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