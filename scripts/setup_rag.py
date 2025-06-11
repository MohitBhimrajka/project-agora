# FILE: scripts/setup_rag.py

import os
import glob
import time
from pathlib import Path
from dotenv import set_key, find_dotenv
import vertexai
from vertexai import rag
from google.cloud import storage
from google.api_core.exceptions import Conflict, NotFound

# --- LLM PARSER CONFIGURATION ---
# This is the custom prompt we designed in the previous step.
CUSTOM_PARSING_PROMPT = """
You are a factual data extractor for a technical software development kit (SDK) documentation.
Your task is to extract key information from the provided documents, which include technical guides, API references, and code examples for the Google Agent Development Kit (ADK).
Present the extracted information in a structured format. Preserve the original structure of the document, including headings, lists, and code blocks using Markdown.
Your primary focus is to extract the following key data types exactly as they appear in the text:
- Specific class names (e.g., `Agent`, `LlmAgent`, `VertexAiRagRetrieval`)
- Method or function names (e.g., `create_ticket`, `rag.import_files`)
- Technical concepts and keywords (e.g., "multi-agent orchestration", "state management", "RAG", "BigQuery")
- Parameters and arguments (e.g., `model`, `instruction`, `tool_context`)
- Code snippets and examples
Do not analyze, interpret, summarize, or give opinions on the content. Your role is to extract only what the document explicitly says. Do not add any information that is not present in the source text.
"""
# Using a cost-effective but capable model for parsing.
PARSER_MODEL_NAME = "gemini-2.0-flash-001"
# --------------------------------

def upload_folder_to_gcs(bucket_name, source_folder, destination_prefix=""):
    """Uploads files from a local folder to a GCS bucket, skipping existing files."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    source_path = Path(source_folder)
    filepaths = [p for p in source_path.rglob("*") if p.is_file() and not p.name.startswith('.')]

    print(f"INFO: Checking {len(filepaths)} files for upload from '{source_folder}'...")

    upload_count = 0
    for filepath in filepaths:
        destination_blob_name = os.path.join(destination_prefix, filepath.relative_to(source_path))
        blob = bucket.blob(destination_blob_name)
        if not blob.exists():
            blob.upload_from_filename(str(filepath))
            upload_count += 1
    
    if upload_count > 0:
        print(f"INFO: Successfully uploaded {upload_count} new files to gs://{bucket_name}/{destination_prefix}")
    else:
        print("INFO: All files already up-to-date in Google Cloud Storage.")

def create_gcs_bucket_if_not_exists(bucket_name, project_id, location):
    """Creates a GCS bucket if it does not already exist."""
    storage_client = storage.Client(project=project_id)
    try:
        storage_client.get_bucket(bucket_name)
        print(f"INFO: GCS Bucket '{bucket_name}' already exists.")
    except NotFound:
        print(f"INFO: GCS Bucket '{bucket_name}' not found. Creating...")
        storage_client.create_bucket(bucket_name, project=project_id, location=location)
        print(f"INFO: Created GCS Bucket '{bucket_name}'.")

def write_to_env(key: str, value: str):
    """Writes a key-value pair to the .env file in the project root."""
    dotenv_path = find_dotenv()
    if not dotenv_path:
        dotenv_path = ".env"
        Path(dotenv_path).touch()
    set_key(dotenv_path, key, value, quote_mode="never")
    print(f"INFO: Wrote '{key}={value}' to {dotenv_path}")

def get_or_create_rag_corpus(display_name: str) -> rag.RagCorpus:
    """Retrieves an existing RAG corpus by display name or creates a new one."""
    corpora = rag.list_corpora()
    for existing_corpus in corpora:
        if existing_corpus.display_name == display_name:
            print(f"INFO: Found existing RAG Corpus '{display_name}' with name: {existing_corpus.name}")
            return existing_corpus
    print(f"INFO: RAG Corpus '{display_name}' not found. Creating a new one...")
    new_corpus = rag.create_corpus(display_name=display_name)
    print(f"INFO: Created new RAG Corpus with name: {new_corpus.name}")
    return new_corpus

def setup():
    """Main function to set up the RAG corpus."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")

    if not all([project_id, location, bucket_name]):
        raise ValueError("GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_STORAGE_BUCKET must be set.")

    vertexai.init(project=project_id, location=location)

    print("\n--- Step 1: Setting up Google Cloud Storage ---")
    create_gcs_bucket_if_not_exists(bucket_name, project_id, location)
    kb_source_folder = "data/pdf"
    gcs_destination_prefix = "rag_knowledge_base"
    upload_folder_to_gcs(bucket_name, kb_source_folder, gcs_destination_prefix)
    gcs_uri = f"gs://{bucket_name}/{gcs_destination_prefix}"

    print("\n--- Step 2: Setting up Vertex AI RAG Corpus ---")
    corpus_display_name = "adk_knowledge_base_corpus"
    corpus = get_or_create_rag_corpus(corpus_display_name)
    
    print("\n--- Step 3: Updating Environment File ---")
    write_to_env("RAG_CORPUS_NAME", corpus.name)

    print(f"\n--- Step 4: Importing files with LLM Parser ---")
    
    try:
        # --- THIS IS THE CORRECTED SECTION ---
        # Configure the transformation and LLM parser as per the documentation
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=1024,
                chunk_overlap=200,
            ),
        )

        llm_parser_config = rag.LlmParserConfig(
            model_name=PARSER_MODEL_NAME,
            custom_parsing_prompt=CUSTOM_PARSING_PROMPT,
        )

        import_op = rag.import_files(
            corpus.name,
            [gcs_uri],
            transformation_config=transformation_config,
            llm_parser=llm_parser_config, # Use the llm_parser parameter
        )
        # -------------------------------------

        print(f"INFO: File import process started (Job ID: {import_op.name}). This is an async operation.")
        print("INFO: Polling for completion status... (This may take a few minutes)")
        
        import_job = rag.get_import_job(import_op.name)

        while import_job.state == rag.ImportState.RUNNING:
            print("  - Import job is still running...")
            time.sleep(30)
            import_job = rag.get_import_job(import_op.name)
        
        if import_job.state == rag.ImportState.SUCCEEDED:
            print("✅ File import completed successfully.")
            print("\n✅✅✅ RAG Corpus setup complete! ✅✅✅")
        else:
            print(f"❌ File import failed with state: {import_job.state}")
            if import_job.error:
                 print(f"  - Error details: {import_job.error.message}")

    except Exception as e:
        print(f"❌ An error occurred during RAG file import: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    setup()