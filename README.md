# ADK Copilot: A Reusable Multi-Agent Framework built with Google ADK

![Category](https://img.shields.io/badge/Category-Automation%20of%20Complex%20Processes-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)

This repository showcases a powerful, reusable framework built from the ground up with the **Google Agent Development Kit (ADK)**. It demonstrates how to leverage the ADK to architect and orchestrate a sophisticated team of AI specialists that can automate complex processes.

The primary implementation, **ADK Copilot**, serves as an expert assistant for the ADK itself. However, the core of this project is a **domain-agnostic framework** that you can adapt to create your own specialized AI assistants, all while using the ADK's robust orchestration capabilities.

<!-- **[➡️ Watch the Demo Video Here](https://your-video-link.com)** -->
---

## The ADK-Powered Framework

This project's innovation lies in using the ADK not just to build a single agent, but to create a **blueprint for collaborative AI systems**. The framework provides a pre-built, stateful orchestration engine, allowing you to focus on defining your agents' unique skills rather than the complex mechanics of their interaction.

This architecture is designed for extension. You can create your own powerful assistant by:
1.  **Defining Agent Expertise:** Update the prompts in the modular sub-agents (`problem_solver`, `code_generator`, etc.) to give them new specializations.
2.  **Providing Custom Knowledge:** Swap the included documentation and data for your own, and the automated setup scripts will create a new knowledge base for your agents.
3.  **Expanding the Team:** The ADK's design makes it simple to add new specialist agents and register them with the central orchestrator.

## Key Features: How the ADK Enables an Advanced Architecture

### A Modular Team of AI Specialists, Enabled by ADK
The framework's core is an `orchestrator_agent` that manages a team of sub-agents. This pattern, made clean and simple by the ADK's `AgentTool`, allows for a clear separation of concerns, making the system easy to extend and maintain.

### Supercharging ADK Agents with Vertex AI
To give our ADK agents powerful tools, we integrated them with Google Cloud's best-in-class services:
*   **The Librarian Agent:** This ADK agent wields the **Vertex AI RAG Engine**, allowing it to perform true semantic search across a vast corpus of documents.
*   **The Veteran Agent:** This ADK agent connects to **BigQuery**, using its native **vector search** capabilities to recall solutions from a historical database, giving the system a powerful, experience-based memory.

### Seamless Deployment for ADK Applications
The framework includes a complete CI/CD-ready setup for your ADK applications.
*   **For Development:** A single command deploys the system to **Cloud Run**, providing a web UI for rapid testing.
*   **For Production:** A second script provides a path to a managed, scalable endpoint on the **Vertex AI Agent Engine**.

### One-Command Setup for Your ADK Environment
To accelerate development, a master `setup_environment.sh` script automates the entire backend creation on Google Cloud, saving hours of manual configuration of data sources for your agents.

## The ADK Copilot: An Example in Action

Our pre-configured implementation demonstrates this framework's power by tackling the complex process of developer support for the Google Agent Development Kit.

### Agent Architecture

![ADK Copilot Architecture](architecture_diagram.png)

The system is orchestrated by a main `orchestrator_agent` which delegates tasks to the following pre-configured specialists:
*   **`ticket_analysis_agent`**: Analyzes the initial developer request.
*   **`knowledge_retrieval_agent`**: Searches the ADK documentation via Vertex AI RAG.
*   **`db_retrieval_agent`**: Searches a BigQuery DB of historical ADK issues.
*   **`problem_solver_agent`**: Synthesizes context to solve technical problems.
*   **`code_generator_agent`**: Generates complete, multi-file ADK code.

### Key Features

-   **Reusable Multi-Agent Framework:** A robust, state-driven architecture that can be easily adapted to any knowledge domain.
-   **Stateful, Multi-Turn Workflow:** Manages a `SupportTicket` state object to ensure a logical, fault-tolerant progression from problem to solution.
-   **Dual-Source Knowledge Retrieval:** Combines real-time document search (RAG) with historical data lookup (BigQuery vector search) for comprehensive context.
-   **Fully Automated Cloud Setup:** A single shell script (`setup_environment.sh`) handles the creation of all necessary data, Google Cloud Storage, BigQuery tables, and the Vertex AI RAG Corpus, making setup seamless.
-   **Production-Ready Deployment Options:** Includes scripts to deploy the system to both Google Cloud Run (for development) and the scalable Vertex AI Agent Engine (for production).

> **Note on Included Knowledge Base:** The knowledge base for the ADK Copilot implementation is generated by scraping the publicly available [Google ADK documentation website](https://google.github.io/adk-docs/). All content rights belong to the original authors.

## Technologies Used

*   **Core Framework:** Google Agent Development Kit (ADK)
*   **Language:** Python 3.11+
*   **AI Models:** Google Gemini 1.5 Pro & 1.5 Flash (via Vertex AI)
*   **Data & Retrieval:**
    *   Vertex AI RAG (Retrieval-Augmented Generation)
    *   Google BigQuery (for vector search on historical data)
    *   Google Cloud Storage (for RAG document storage)
*   **Deployment:**
    *   Vertex AI Agent Engine
    *   Google Cloud Run
*   **Tooling:** Poetry, GCloud SDK

## Setup and Installation

Follow these steps to set up the project environment and all necessary data backends.

### 1. Prerequisites

-   Python 3.11+
-   [Poetry](https://python-poetry.org/docs/) for dependency management.
-   A Google Cloud Project with the AI Platform API enabled.
-   The [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated (`gcloud auth application-default login`).

### 2. Configure Environment Variables

Copy the example environment file. **This is a mandatory step.**

```bash
cp .env.example .env
```

Now, edit the newly created `.env` file with your specific Google Cloud project details.

```dotenv
# .env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-gcp-project-id
RAG_CORPUS_NAME="" # This will be auto-populated by the setup script
BQ_PROJECT_ID=your-gcp-project-id
BQ_DATASET_ID=adk_copilot_dataset
CRM_API_KEY="your-crm-api-key-here" # Optional, not used in core logic
```

**Note:** The `GOOGLE_CLOUD_STORAGE_BUCKET` must be a globally unique name. Using your project ID as a prefix is a good practice to ensure uniqueness.

### 3. Install Dependencies

Use Poetry to create a virtual environment and install all required Python packages.

```bash
poetry install
```

### 4. Run the Automated Environment Setup

This final step runs a shell script that automates the entire backend setup process. It generates mock data and configures your Google Cloud services (BigQuery and RAG).

First, make the script executable:
```bash
chmod +x setup_environment.sh
```

Now, run the script:
```bash
./setup_environment.sh
```

This script will perform the following actions:
1.  **Scrape Docs:** Run `scripts/scrape_adk_docs.py` to build the `data/knowledge_base`.
2.  **Create Mock DB:** Run `scripts/create_mock_db.py` to generate `data/resolved_tickets.csv`.
3.  **Setup BigQuery:** Run `scripts/setup_bigquery.py` to create the dataset and table in your GCP project and upload the CSV data.
4.  **Setup RAG:** Run `scripts/setup_rag.py` to create a GCS bucket, upload the knowledge base, create a Vertex AI RAG Corpus, and **automatically write the new `RAG_CORPUS_NAME` back to your `.env` file.**

After this script completes, your entire backend and data infrastructure will be ready to use.

## Running the Agent

You can interact with the agent using the ADK's built-in web interface.

```bash
# Make sure you are in the project's virtual environment
# poetry shell

adk web
```

Navigate to `http://localhost:8000` in your browser and select the `adk_copilot` agent from the dropdown menu.

### Example Interactions

-   **Problem Solving:** "My deployment is failing with a 403 Permission Denied error when trying to deploy my agent to Vertex AI. I've checked my service account permissions but I'm still getting this error."
-   **Code Generation:** "Write me an agent that uses a custom tool to get the current weather and provides personalized clothing recommendations based on the forecast."
-   **Architecture Guidance:** "I need to build a multi-agent system that processes customer feedback. What's the best approach using ADK?"
-   **Debugging Help:** "My agent is running but the tools aren't being called correctly. Can you help me troubleshoot?"

## Findings & Learnings

Building this project was a deep dive into the practicalities of multi-agent system design. Here are our key takeaways:

1.  **The Orchestrator is a State Machine:** The most critical learning was that a robust orchestrator is essentially a state machine. By managing a `status` field (e.g., "New", "Analyzing", "Pending Solution") in the shared state, we could create a reliable, sequential, and fault-tolerant workflow. Without this, agents would fire unpredictably.
2.  **Isolate Specialized Tools:** Early on, we had issues mixing the `VertexAiRagRetrieval` tool with other custom tools in a single agent. The solution was architectural: create highly specialized "tool-runner" agents (like `knowledge_retrieval_agent`) whose only job is to expose one complex tool. This simplified the orchestrator's job and resolved API constraints.
3.  **Prompt Engineering is System Design:** The orchestrator's prompt isn't just an instruction; it's the central logic of the application. We spent significant time refining it to be deterministic, forcing a specific sequence of actions based on the current state. This was more effective than letting the model "decide" the entire workflow on its own.
4.  **Automation is Key for Judges:** We knew that a complex backend (BigQuery, RAG, GCS) would be hard for judges to set up. Investing time in the `setup_environment.sh` script was crucial to ensure our project was easily testable, a key requirement for the hackathon.

## Project Structure

A comprehensive overview of the repository structure:

```
adk-copilot/
├── adk_copilot/                    # Core source code for the agent system
│   ├── agent.py                    # Main orchestrator agent definition
│   ├── prompts.py                  # System prompts for all agents
│   ├── entities/                   # Data models and structures
│   │   ├── ticket.py              # SupportTicket Pydantic model
│   │   └── __init__.py
│   ├── sub_agents/                 # Specialized sub-agent implementations
│   │   ├── README.md              # Sub-agents documentation
│   │   ├── ticket_analysis/        # Analyzes and categorizes user requests
│   │   │   ├── agent.py
│   │   │   └── __init__.py
│   │   ├── knowledge_retrieval/    # RAG-based documentation search
│   │   │   ├── agent.py
│   │   │   └── __init__.py
│   │   ├── db_retrieval/          # BigQuery historical data search
│   │   │   ├── agent.py
│   │   │   └── __init__.py
│   │   ├── problem_solver/        # Synthesizes solutions from context
│   │   │   ├── agent.py
│   │   │   └── __init__.py
│   │   ├── code_generator/        # Generates code examples and implementations
│   │   │   ├── agent.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── tools/                     # Custom Python function tools
│   │   ├── tools.py               # RAG search and BigQuery tools
│   │   ├── README.md              # Tools documentation
│   │   └── __init__.py
│   └── __init__.py
├── scripts/                       # Environment setup and data preparation
│   ├── README.md                  # Scripts documentation
│   ├── scrape_adk_docs.py         # Scrapes ADK documentation for knowledge base
│   ├── create_mock_db.py          # Generates mock historical ticket data
│   ├── setup_bigquery.py         # Creates BigQuery dataset and uploads data
│   └── setup_rag.py              # Sets up Vertex AI RAG corpus and GCS bucket
├── data/                          # Data files and knowledge base
│   ├── README.md                  # Data documentation
│   ├── knowledge_base/            # Scraped ADK documentation files
│   │   ├── adk_handbook.md        # Comprehensive ADK handbook
│   │   ├── adk-docs.md           # Main documentation file
│   │   ├── adk-docs_*.md         # Specific documentation sections
│   │   ├── *.txt                 # Additional knowledge files
│   │   └── rag.txt               # RAG-specific documentation
│   ├── pdf/                      # PDF versions of knowledge base files
│   └── resolved_tickets.csv       # Mock historical support tickets
├── deployment/                    # Deployment scripts and configurations
│   ├── README.md                  # Deployment documentation
│   ├── deploy_cloud_run.sh        # Cloud Run deployment script
│   └── deploy_vertex_agents.sh    # Vertex AI deployment script
├── setup_environment.sh           # Automated environment setup script
├── pyproject.toml                 # Poetry configuration and dependencies
├── .env.example                   # Example environment variables file
└── README.md                      # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.