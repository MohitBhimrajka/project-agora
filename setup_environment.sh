#!/bin/bash

# This script orchestrates the entire setup for the data backend.
# It ensures that commands are run in the correct order.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "🔵 Phase 1: Generating local mock database file..."
python3 scripts/create_mock_db.py

echo "🟢 Phase 1 Complete."
echo "---------------------------------"
echo "🔵 Phase 2: Setting up BigQuery..."
echo "   This will create a dataset and upload the mock data."
python3 scripts/setup_bigquery.py

echo "🟢 Phase 2 Complete."
echo "---------------------------------"
echo "🔵 Phase 3: Setting up Vertex AI RAG Corpus..."
echo "   This involves creating a GCS bucket, uploading knowledge base files, and creating a RAG corpus."
echo "   NOTE: RAG corpus creation and file ingestion can take several minutes."
python3 scripts/setup_rag.py

echo "---------------------------------"
echo "✅✅✅ Environment setup is complete! ✅✅✅"
echo "Your BigQuery table is ready and your RAG corpus has been created and is processing your files."
echo "Your .env file has been updated with the RAG_CORPUS_NAME."