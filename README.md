# ADK Copilot: A Reusable Framework for Autonomous AI Teams

> ### Built for ADK Developers, by an ADK-powered AI Team.

![Category](https://img.shields.io/badge/Category-Automation%20of%20Complex%20Processes-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)

This project showcases a powerful, reusable framework built with the **Google Agent Development Kit (ADK)** to architect and orchestrate sophisticated teams of AI specialists that can automate complex, end-to-end workflows.

**This is not just a chatbot. It is a blueprint for building autonomous, collaborative AI systems.**

---

### TL;DR: Quickstart

For experienced developers who want to get running immediately:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd adk-copilot

# 2. Configure your environment
cp .env.example .env
# --> EDIT .env and set your GCP_PROJECT_ID and a unique BUCKET_NAME <--

# 3. Install dependencies
poetry install

# 4. Provision the cloud backend (this will take several minutes)
./setup_environment.sh

# 5. Run the agent
adk web
```

![ADK Copilot Architecture v2](architecture_diagram_v2.png)
_The architecture: An ADK Orchestrator managing a full development lifecycle with a code review loop._

## Who is This Framework For?

This repository is designed for:

- **AI Engineers & Developers** looking to build robust, multi-agent systems that go beyond simple request-response.
- **Teams wanting to automate complex internal processes** (like developer support, data analysis, or content creation) with a reliable, stateful AI workforce.
- **Architects seeking a production-ready blueprint** for deploying agentic workflows on Google Cloud.

## The ADK Copilot: An Example in Action

The best way to understand the framework is to see it work. The pre-configured ADK Copilot is designed to automate the complex process of developer support with an entire AI team.

### Meet the AI Team
The orchestrator manages a team of six highly specialized agents:

*   **`ticket_analysis_agent` (The Analyst):** Performs triage on user requests, with the ability to read linked files from GCS for deeper context.
*   **`knowledge_retrieval_agent` (The Librarian):** Searches the official ADK documentation using the **Vertex AI RAG Engine**.
*   **`db_retrieval_agent` (The Veteran):** Recalls historical solutions from a **BigQuery** database using vector search.
*   **`code_generator_agent` (The Engineer):** Designs a plan, visualizes it, and generates multi-file ADK agent code.
*   **`code_reviewer_agent` (The QA Lead):** Automatically reviews generated code for quality and correctness.
*   **`problem_solver_agent` (The Synthesizer):** Provides step-by-step solutions for non-code-related issues.

### Example Interaction
Here's a walkthrough of the new, end-to-end code generation workflow:

> **User:** Write me an agent that uses an external API to get the current price of Bitcoin.

> **Agent:** Thank you for your request... I've found some relevant information. I am now ready to formulate a plan. Shall I proceed?

> **User:** Yes, please.

> **Agent:** Excellent. Here is the proposed architecture for your `CryptoPriceAgent`. I will create a main agent that uses a custom tool to call the CoinDesk API. This will require the `requests` library. Does this plan look good?
>

> **User:** The plan and diagram look perfect. Go ahead and build it.

> **Agent:** Great. I will now generate the complete code and pass it for a final quality check.
>
> *Behind the scenes, the Engineer generates the code. The QA Lead then reviews it against the style guide and approves it.*
>
> **Agent:** The code has been generated and has passed all quality checks. Here is the complete, multi-file agent:
>
> `==== FILE: crypto_price_agent/agent.py ====`
> ... (and so on)

## The Core Idea: A Framework for AI Teams

The goal of this project was to move beyond simple "copilots" and build a system that mimics a real, high-functioning software development team. This framework uses the **Google Agent Development Kit** to create a central `orchestrator_agent` that manages a stateful workflow across a team of swappable, specialist sub-agents.

The heavy lifting—the interactive state machine, the parallel data retrieval, the dynamic diagram generation, the automated quality assurance, and the cloud infrastructure setup—is already done.

## Key Architectural Pillars & Features

I designed the framework around four core pillars that make it a robust and production-ready system.

#### 1. Build Reliable Workflows with a State Machine
Reliability is everything. The orchestrator is a strict state machine governed by its ADK prompt. It moves tasks through a granular lifecycle (`New` -> `Analyzing` -> `AwaitingConfirmation` -> `Generating` -> `Reviewing`). Crucially, it communicates its progress and **waits for user approval** at key checkpoints, creating a collaborative and controllable workflow.

#### 2. Understand Deeper with Multi-Modal Input
The `ticket_analysis_agent` can understand more than just text. Users can provide a link to a log file or code file in **Google Cloud Storage** (`gs://...`). The agent uses a tool to read the file's content, incorporating it into its analysis for a much deeper understanding of the user's problem.

#### 3. Communicate Visually with Dynamic Diagrams
A good developer team communicates its plan visually. When asked to generate code, the `code_generator_agent` first outputs a textual plan *and* **Mermaid syntax** for an architecture diagram. A custom tool then uses Playwright to render this syntax into a PNG, which is shown to the user. This "show, don't just tell" approach is a core feature.

#### 4. Guarantee Quality with an Automated Code Reviewer
Generated code is not trusted blindly. After the `code_generator_agent` writes the code, it is immediately passed to a dedicated `code_reviewer_agent`. This QA agent analyzes the code against a formal **style guide**, checking for correctness, security, and best practices, ensuring a high-quality output every time.

## Getting Started (Detailed Steps)

Follow these steps to set up and run the ADK Copilot on your local machine.

### Step 1: Prerequisites

- **Python 3.11+**
- **Poetry** for dependency management.
- An authenticated **Google Cloud SDK** (`gcloud auth application-default login`).

### Step 2: Configuration

**Clone the Repository:**
```bash
git clone <your-repo-url>
cd adk-copilot
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

Once the server starts, open the URL in your browser and select `adk_copilot` from the agent dropdown list.

## Customizing the Framework
This project's greatest strength is its adaptability. To create your own specialized assistant:

1.  **Provide New Knowledge:** Replace the files in `data/knowledge_base` and update the data generation script in `scripts/create_mock_db.py`.
2.  **Define New Specialists:** Edit the prompts in `adk_copilot/sub_agents/` to change agent expertise and behavior.
3.  **Run the Setup Script:** Execute `./setup_environment.sh` to build a new cloud backend for your custom agent.

## Testing and Deployment

*   **Evaluation:** Run `poetry run pytest eval`.
*   **Deployment:** Use the scripts in the `deployment/` directory to deploy to **Google Cloud Run** or the **Vertex AI Agent Engine**. See `deployment/README.md`.

## Repository Structure

The repository is organized to separate core logic from data, scripts, and deployment configurations.

```
mohitbhimrajka-adk-copilot/
├── .github/                 # GitHub templates for issues and PRs.
├── adk_copilot/             # Core application source code.
│   ├── agent.py             # Main orchestrator agent.
│   ├── prompts.py           # Centralized prompts for all agents.
│   ├── entities/            # Pydantic data models (SupportTicket).
│   ├── sub_agents/          # Specialist agents (Analyst, Engineer, etc.).
│   └── tools/               # Custom tools (BigQuery search, diagram gen, etc.).
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
- [ ] **GitHub Integration Hub**: Comprehensive GitHub integration for automated code reviews, issue management, and CI/CD pipeline orchestration
- [ ] **Federated Agent Networks**: Support for distributed agent teams across multiple organizations or cloud environments
- [ ] **Industry-Specific Templates**: Pre-configured agent teams for specific domains (healthcare, finance, legal, etc.)

### Community Contributions Welcome
We're particularly interested in contributions that:
- Add new specialized agents for different domains
- Improve the reliability and robustness of existing tools
- Enhance the developer experience with better debugging and monitoring
- Expand integration capabilities with popular enterprise tools

See our [Contributing Guide](CONTRIBUTING.md) for details on how to get involved!

## Disclaimer

This project was developed for the Google ADK Hackathon. It is provided for illustrative purposes and is not intended for production use without further testing and hardening.
