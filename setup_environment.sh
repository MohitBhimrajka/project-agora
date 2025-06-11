#!/bin/bash
set -e

echo "🔵 Phase 1: Scraping ADK documentation to build knowledge base..."
python3 scripts/scrape_adk_docs.py

echo "🟢 Phase 1 Complete."
echo "---------------------------------"
echo "🔵 Phase 2: Generating local mock database file..."
python3 scripts/create_mock_db.py

echo "🟢 Phase 2 Complete."
echo "---------------------------------"
echo "🔵 Phase 3: Setting up BigQuery..."
python3 scripts/setup_bigquery.py

echo "🟢 Phase 3 Complete."
echo "---------------------------------"
echo "🔵 Phase 4: Setting up Vertex AI RAG Corpus..."
python3 scripts/setup_rag.py

echo "---------------------------------"
echo "✅✅✅ Environment setup is complete! ✅✅✅"