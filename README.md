# **Project Agora: A Framework for Multi-Agent Workflows**

> ### A reference implementation for orchestrating hierarchical multi-agent systems on Google Cloud using the Agent Development Kit (ADK).

[![Category](https://img.shields.io/badge/Category-Automation%20of%20Complex%20Processes-blue)](https://devpost.com/) [![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE) [![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/MohitBhimrajka/project-agora)

This project showcases a powerful, reusable framework for architecting and orchestrating hierarchical multi-agent systems with the **Google Agent Development Kit (ADK)**. It provides a robust pattern for automating complex, end-to-end workflows by composing specialized, tool-using agents.

**This is not just a chatbot. It is an architectural blueprint for building stateful, collaborative agentic systems.**

> **Why Agora?**
> In ancient Greece, the **Agora** was the central public square—a hub of assembly, dialogue, and commerce where specialized craftsmen and thinkers came together to solve problems. This framework provides a digital Agora: a central orchestration hub where specialized AI agents assemble to collaborate, reason, and execute complex tasks, harnessing their collective intelligence.

---

### TL;DR: Quickstart

For experienced developers who want to get running immediately:

```bash
# 1. Clone the repository
git clone https://github.com/MohitBhimrajka/project-agora.git
cd project-agora

# 2. Configure your environment
cp .env.example .env
# --> EDIT .env and set your GCP_PROJECT_ID and a unique BUCKET_NAME <--

# 3. Install dependencies
poetry install

# 4. Provision the cloud backend (this will take several minutes)
./setup_environment.sh

# 5. Run the agent
adk web # And select 'project_agora' from the dropdown
```

![Project Agora Architecture](agora_architecture.png)
_The architecture: A root agent orchestrating specialized sub-agents via the `AgentTool` class._

## Who is This Framework For?

This repository is designed for:

- **AI Engineers & Developers** looking to build robust multi-agent systems that go beyond simple request-response patterns.
- **Solutions Architects** seeking a production-ready architectural pattern for deploying agentic workflows on Google Cloud.
- **Teams wanting to automate complex internal processes** (like developer support, data analysis, or content creation) with reliable, stateful agents.

## Project Agora: An Example Workflow

The best way to understand the framework is to observe its agentic workflow. Project Agora is pre-configured to automate the complex process of developer support through a structured, multi-agent system.

### The Agent Hierarchy
The root `orchestrator_agent` manages a set of six specialized sub-agents, each exposed to the orchestrator as an `AgentTool`:

*   **`ticket_analysis_agent` (The Triage Agent):** Performs initial request analysis and classification. It uses a custom `read_user_file` tool to process contextual data from Google Cloud Storage URIs (`gs://...`).
*   **`knowledge_retrieval_agent` (The RAG Agent):** Executes queries against a knowledge base using the ADK's built-in **`VertexAiRagRetrieval`** tool, grounded on official ADK documentation.
*   **`db_retrieval_agent` (The Vector Search Agent):** Recalls historical solutions by executing a **`COSINE_DISTANCE`** vector search against a **BigQuery** table of past ticket embeddings.
*   **`code_generator_agent` (The Code Generation Agent):** Designs a plan with a Mermaid diagram for user approval, then generates complete, multi-file ADK agent code based on a strict style guide.
*   **`code_reviewer_agent` (The QA Agent):** A dedicated agent that programmatically reviews generated code against a formal style guide to ensure correctness and adherence to best practices.
*   **`problem_solver_agent` (The Synthesis Agent):** A stateless `LlmAgent` that synthesizes context from all prior steps to formulate step-by-step text solutions for non-code issues.

### Example Inference Chain
Here's a walkthrough of the end-to-end code generation workflow:

> **User:** Write me an agent that uses an external API to get the current price of Bitcoin.

> **Agora:** Thank you for your request... I have retrieved relevant context. I am now ready to formulate an execution plan. Shall I proceed?

> **User:** Yes, please.

> **Agora:** Excellent. Here is the proposed architecture for your `CryptoPriceAgent`. I will create a root agent that utilizes a custom tool to call the CoinDesk API. This will require the `requests` library. Does this plan look correct?
>

> **User:** The plan and diagram look perfect. Go ahead and build it.

> **Agora:** Great. I will now invoke the code generation agent and pass the output to the quality assurance agent for review.
>
> *[Behind the scenes: The `code_generator_agent` is invoked. Its string output is then passed as an argument to the `code_reviewer_agent`.]*
>
> **Agora:** The generated code has passed all quality checks. Here is the complete, multi-file agent:
>
> `==== FILE: crypto_price_agent/agent.py ====`
> ... (and so on)

## The Core Architectural Pattern

This framework implements a **hierarchical agent topology**. It uses the Google ADK to create a central `orchestrator_agent` that directs a stateful workflow across a set of swappable, specialized sub-agents. Each sub-agent is wrapped in an **`AgentTool`**, allowing the orchestrator to invoke them just like any other tool.

The framework handles the complex implementation details: the stateful inference chain, parallel tool execution for data retrieval, dynamic diagram generation via a custom tool, an automated QA review loop, and the declarative cloud infrastructure setup.

## Key Technical Features

The framework is built on four pillars that ensure robustness and production-readiness.

#### 1. Prompt-Defined State Machine for Reliability
The orchestrator's behavior is governed by a strict state machine defined within its instruction prompt. It moves tasks through a granular lifecycle (`New` -> `Analyzing` -> `AwaitingConfirmation`). Critically, the prompt instructs the agent to **wait for explicit user confirmation** at key transition points, creating a controllable and auditable inference chain.

#### 2. Contextual Grounding with Multi-Modal Input
The `ticket_analysis_agent` can ground its analysis on more than just text. By using a custom tool (`read_user_file`), it can ingest the content of log files or code files provided by the user via a **Google Cloud Storage** URI (`gs://...`), enabling a deeper understanding of the problem space.

#### 3. Visual Execution Plans with Dynamic Diagrams
The system communicates its execution plan visually. The `code_generator_agent` first outputs a plan and **Mermaid syntax** for an architecture diagram. A custom tool then renders this into a PNG and returns a public URL. This "show, don't just tell" approach provides transparency into the agent's reasoning process.

#### 4. Automated Quality Gates with a Reviewer Agent
To ensure output quality, generated code is not trusted implicitly. After the `code_generator_agent` writes the code, it is immediately passed to the dedicated `code_reviewer_agent`. This QA agent programmatically analyzes the code against a formal **style guide**, ensuring correctness and adherence to best practices before the result is presented to the user.

## Getting Started (Detailed Steps)

Follow these steps to set up and run Project Agora on your local machine.

### Step 1: Prerequisites

- **Python 3.11+**
- **Poetry** for dependency management.
- An authenticated **Google Cloud SDK** (`gcloud auth application-default login`).

### Step 2: Configuration

**Clone the Repository:**
```bash
git clone https://github.com/MohitBhimrajka/project-agora.git
cd project-agora
```

**Create an Environment File:** Copy the example `.env` file.
```bash
cp .env.example .env
```

**Edit `.env`:** Open the new `.env` file and set the following required values:
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
- `GOOGLE_CLOUD_STORAGE_BUCKET`: A globally unique name for a new GCS bucket that will be created.
- `BQ_PROJECT_ID`: Set this to your Google Cloud Project ID.

### Step 3: Installation & Backend Setup

**Install Dependencies:**
```bash
poetry install
```

**Provision Cloud Resources:** This master script will create the GCS bucket, BigQuery dataset, and Vertex AI RAG Corpus needed for the agent. This may take 5-10 minutes.
```bash
./setup_environment.sh
```

### Step 4: Running the Agent

Start the local web interface provided by the ADK CLI.
```bash
adk web
```

Once the server starts, open the URL in your browser and select `project_agora` from the agent dropdown list.

## Customizing the Framework
This project's adaptability is its greatest strength. To create your own specialized agentic workflow:

1.  **Provide a New Knowledge Base:** Replace the files in `data/knowledge_base` and update the mock data generation in `scripts/create_mock_db.py`.
2.  **Define New Sub-Agents:** Edit the prompts and tools in `project_agora/sub_agents/` to change agent capabilities and behavior.
3.  **Run the Setup Script:** Execute `./setup_environment.sh` to provision a new cloud backend for your custom system.

## Testing and Deployment

*   **Evaluation:** Run `poetry run pytest eval`.
*   **Deployment:** Use the scripts in the `deployment/` directory to deploy to **Google Cloud Run** or the **Vertex AI Agent Engine**. See `deployment/README.md`.

## Repository Structure

The repository is organized to separate core agent logic from data, scripts, and deployment configurations.

```
project-agora/
├── .github/                 # GitHub templates for issues and PRs.
├── project_agora/           # Core application source code.
│   ├── agent.py             # The root orchestrator agent.
│   ├── prompts.py           # Instruction prompts for all agents.
│   ├── entities/            # Pydantic data models for state management.
│   ├── sub_agents/          # Specialized sub-agents, each wrapped in an AgentTool.
│   └── tools/               # Custom tools for data access and rendering.
├── deployment/              # Scripts for Cloud Run & Agent Engine deployment.
├── eval/                    # Evaluation suite for testing agent performance.
│   └── data/                # Test cases for evaluation.
├── scripts/                 # Automation scripts for setup and data prep.
├── cleanup.sh               # Reverses the setup script.
├── CONTRIBUTING.md
├── LICENSE
├── Makefile                 # Simplified commands for developers.
├── pyproject.toml           # Project dependencies and configuration.
└── README.md                # This file.
```

## 🛣️ Roadmap

This framework is a living project with exciting enhancements planned for the future. We welcome community input and contributions!

### Long-term Aspirations
- [ ] **GitHub Tool Integration**: Comprehensive GitHub integration for automated code reviews, issue management, and CI/CD pipeline orchestration.
- [ ] **Federated Agent Topologies**: Support for distributed agent systems across multiple cloud environments.
- [ ] **Industry-Specific Implementations**: Pre-configured agent hierarchies for specific domains (healthcare, finance, legal, etc.).

### Community Contributions Welcome
We're particularly interested in contributions that:
- Add new specialized sub-agents for different domains.
- Improve the reliability and robustness of existing custom tools.
- Enhance the developer experience with better debugging and monitoring.
- Expand integration capabilities with popular enterprise tools.

See our [Contributing Guide](CONTRIBUTING.md) for details on how to get involved!

## Disclaimer

This project was developed for the Google ADK Hackathon. It is provided as a reference implementation and is not intended for production use without further testing and hardening.