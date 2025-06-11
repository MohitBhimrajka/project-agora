import os
import glob
from pathlib import Path
from dotenv import set_key
import vertexai
from vertexai import rag
from google.cloud import storage
from google.api_core.exceptions import Conflict, NotFound

def upload_folder_to_gcs(bucket_name, source_folder, destination_prefix=""):
    """Uploads all files from a local folder to a GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    filepaths = glob.glob(os.path.join(source_folder, "**", "*"), recursive=True)

    for filepath in filepaths:
        if os.path.isfile(filepath):
            destination_blob_name = os.path.join(destination_prefix, os.path.relpath(filepath, source_folder))
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(filepath)
            print(f"File {filepath} uploaded to gs://{bucket_name}/{destination_blob_name}.")

def create_gcs_bucket_if_not_exists(bucket_name, project_id, location):
    """Creates a GCS bucket if it does not already exist."""
    storage_client = storage.Client(project=project_id)
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"GCS Bucket '{bucket_name}' already exists.")
    except NotFound:
        print(f"GCS Bucket '{bucket_name}' not found. Creating...")
        storage_client.create_bucket(bucket_name, project=project_id, location=location)
        print(f"Created GCS Bucket '{bucket_name}'.")

def write_to_env(env_file_path: Path, key: str, value: str):
    """Writes a key-value pair to the specified .env file."""
    set_key(env_file_path, key, value, quote_mode="never")
    print(f"'{key}={value}' written to {env_file_path}")

def setup():
    """Main function to set up the RAG corpus."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")

    if not all([project_id, location, bucket_name]):
        raise ValueError("GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_STORAGE_BUCKET must be set.")

    env_file_path = Path(".env")
    if not env_file_path.exists():
        env_file_path.touch()

    # Initialize Vertex AI API
    vertexai.init(project=project_id, location=location)

    # 1. Setup GCS Bucket and upload KB files
    create_gcs_bucket_if_not_exists(bucket_name, project_id, location)
    kb_source_folder = "data/knowledge_base"
    gcs_destination_prefix = "rag_knowledge_base"
    upload_folder_to_gcs(bucket_name, kb_source_folder, gcs_destination_prefix)

    gcs_uri = f"gs://{bucket_name}/{gcs_destination_prefix}"

    # 2. Create RAG Corpus
    corpus_display_name = "adk_knowledge_base"
    print(f"Creating RAG Corpus '{corpus_display_name}'...")
    try:
        corpus = rag.create_corpus(display_name=corpus_display_name)
        corpus_name = corpus.name
        write_to_env(env_file_path, "RAG_CORPUS_NAME", corpus_name)

        # 3. Import files into the Corpus
        print(f"Importing files from '{gcs_uri}' into corpus '{corpus_name}'...")

        # --- THIS IS THE CORRECTED SECTION ---
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=512,
                chunk_overlap=100,
            )
        )
        rag.import_files(
            corpus_name,
            [gcs_uri],
            transformation_config=transformation_config,
        )
        # -------------------------------------

        print("✅ RAG Corpus setup complete.")

    except Conflict:
        print(f"RAG Corpus '{corpus_display_name}' already exists. Skipping creation.")
        # If you need to find the existing one, you'd list them.
        # For this script, we assume if it exists, it's okay to use.
    except Exception as e:
        print(f"An error occurred during RAG setup: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    setup()