# Scripts Directory

This directory contains all the automation and setup scripts required to prepare the environment and data backends for the Intelligent Support Triage agent.

The primary way to use these scripts is through the main `setup_environment.sh` script in the project root, which runs them in the correct order.

### Scripts

-   **`scrape_adk_docs.py`**:
    -   **Purpose:** To build a local knowledge base for the agent's RAG system.
    -   **Action:** This script crawls the **official Google ADK documentation website** ([https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)). It extracts the main text content from each documentation page and saves it as a markdown file inside `data/knowledge_base/`.
    -   **Disclaimer:** This script is provided for demonstration purposes to build a functional knowledge base from publicly available documentation. Please be respectful of website terms of service and do not use this script excessively or for malicious purposes. All scraped content rights belong to Google and the ADK project authors.

-   **`create_mock_db.py`**:
    -   **Purpose:** Generates a mock database of historical support tickets.
    -   **Action:** Creates a CSV file named `resolved_tickets.csv` inside the `data/` directory. This file contains realistic examples of ADK-related problems and their solutions, which are used to populate the BigQuery database.

-   **`setup_bigquery.py`**:
    -   **Purpose:** Sets up the required Google BigQuery infrastructure.
    -   **Action:**
        1.  Checks if the specified BigQuery dataset exists in your GCP project. If not, it creates it.
        2.  Loads the data from `data/resolved_tickets.csv` into a new table named `resolved_tickets` within that dataset. It will overwrite the table if it already exists to ensure the data is fresh.

-   **`setup_rag.py`**:
    -   **Purpose:** Sets up the Google Cloud Storage and Vertex AI RAG Corpus needed for the knowledge base.
    -   **Action:**
        1.  Checks if the specified GCS bucket exists. If not, it creates it.
        2.  Uploads all files from the local `data/knowledge_base/` directory to the GCS bucket.
        3.  Creates a new Vertex AI RAG Corpus.
        4.  Initiates the import process, telling the RAG service to ingest and index the documentation files from the GCS bucket.
        5.  **Crucially**, it automatically updates the `RAG_CORPUS_NAME` variable in your `.env` file with the resource name of the newly created corpus.