# Deployment Directory

This directory contains the scripts and configuration needed to deploy the Intelligent Support Triage agent to the **Google Cloud Vertex AI Agent Engine**.

## Overview

The deployment process is automated through the `deploy.py` script. This script handles packaging the agent application, configuring its cloud environment, and deploying it as a scalable, serverless endpoint.

## Deployment Script: `deploy.py`

This is the primary script for managing the agent's deployment lifecycle.

### Features

-   **Automated Packaging:** Automatically builds the agent's Python wheel (`.whl`) file using `poetry build`.
-   **Cloud Deployment:** Deploys the agent to Vertex AI Agent Engine, creating a new, managed reasoning engine.
-   **Environment Configuration:** Passes necessary environment variables (like RAG Corpus name and BigQuery details) from your local `.env` file to the cloud environment, ensuring the deployed agent can connect to its data backends.
-   **Agent Deletion:** Provides a command to safely tear down and delete a deployed agent instance to manage cloud resources.

### Prerequisites

Before running the deployment script, ensure you have:
1.  Completed all steps in the main project `README.md`, including running the `setup_environment.sh` script. This ensures your `.env` file is fully populated with the `RAG_CORPUS_NAME` and other necessary values.
2.  Authenticated with Google Cloud with sufficient permissions to manage Vertex AI and IAM resources. The service account used for deployment typically needs roles like `Vertex AI Admin` and `Service Account User`.

### How to Use

#### To Deploy a New Agent:

From the project's root directory, run the following command:

```bash
python3 deployment/deploy.py --create
```

The script will:
1.  Build the application wheel file.
2.  Connect to your configured GCP project.
3.  Deploy the agent to Vertex AI Agent Engine.
4.  Print the full resource name of the deployed agent upon success.

Example output:
```
✅ Agent deployed successfully!
Resource Name: projects/your-gcp-project-id/locations/us-central1/reasoningEngines/1234567890123456789
```
It is recommended to save this resource name for future management.

#### To Delete a Deployed Agent:

You will need the full resource name of the agent you wish to delete.

```bash
python3 deployment/deploy.py --delete --resource_id "projects/your-gcp-project-id/locations/us-central1/reasoningEngines/1234567890123456789"
```

This will permanently delete the agent instance from Vertex AI Agent Engine.