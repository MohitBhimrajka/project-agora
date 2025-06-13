# FILE: adk_copilot/tools/file_reader_tool.py
from google.cloud import storage

def read_user_file(file_uri: str) -> str:
    """
    Reads the content of a user-uploaded file from Google Cloud Storage.

    Args:
        file_uri: The GCS URI of the file (e.g., 'gs://bucket-name/path/to/file.log').

    Returns:
        The content of the file as a string, or an error message.
    """
    if not file_uri.startswith("gs://"):
        return "Error: Invalid GCS URI provided. Must start with 'gs://'."

    try:
        # Assumes the client is authenticated via Application Default Credentials
        client = storage.Client()
        # The URI is in the format gs://<bucket>/<object_path>
        bucket_name, blob_name = file_uri[5:].split("/", 1)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        file_content = blob.download_as_text()
        print(f"INFO: Successfully read content from {file_uri}")
        return file_content
    except Exception as e:
        error_msg = f"Error: Could not read file from GCS URI '{file_uri}'. Details: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg