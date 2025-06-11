# Intelligent Support Triage System

This project is a multi-agent system built with the Google Agent Development Kit (ADK) to intelligently analyze, triage, and generate solutions for customer support tickets.

## Key Features

- **Multi-Agent Architecture:** An Orchestrator agent manages a team of specialized sub-agents for ticket analysis, knowledge retrieval, and solution generation.
- **RAG-Powered Knowledge Base:** Uses Vertex AI Vector Search (via RAG API) to search internal documentation for accurate answers.
- **Historical Data Search:** Connects to BigQuery to find solutions from previously resolved tickets.
- **End-to-End Automation:** Manages the support ticket lifecycle from intake to resolution.

## Setup and Installation

Follow these steps to set up the project environment and all necessary data backends.

### 1. Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/) for dependency management.
- A Google Cloud Project with the AI Platform API enabled.
- The [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated (`gcloud auth application-default login`).

### 2. Configure Environment Variables

Copy the example environment file and fill in your specific Google Cloud project details.

```bash
cp .env.example .env
```

Now, edit the `.env` file with your details:

```
# .env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-gcp-project-id-support-triage
RAG_CORPUS_NAME=""
BQ_PROJECT_ID=your-gcp-project-id
BQ_DATASET_ID=support_tickets_dataset
CRM_API_KEY="your-crm-api-key-here"
```
**Note:** The `GOOGLE_CLOUD_STORAGE_BUCKET` should be a unique name. Using your project ID as a prefix is a good practice.

### 3. Install Dependencies

Use Poetry to create a virtual environment and install all required Python packages.

```bash
poetry install
```

### 4. Run the Environment Setup Script

This final step runs all the necessary scripts to generate mock data and configure your Google Cloud services (BigQuery and RAG).

First, make the script executable:
```bash
chmod +x setup_environment.sh
```

Now, run the script:
```bash
./setup_environment.sh
```
This script will:
1.  Generate the `resolved_tickets.csv` file locally.
2.  Create a BigQuery dataset and table, then upload the CSV data.
3.  Create a GCS bucket, upload your knowledge base files, create a RAG Corpus, and automatically write the new `RAG_CORPUS_NAME` back to your `.env` file.

After this script completes, your entire backend and data infrastructure will be ready.