# Sub-Agents Directory

This directory contains the definitions for all the specialized "worker" agents that are managed by the main `orchestrator_agent`. Each sub-agent is designed to perform a single, specific task within the support ticket resolution workflow.

### Agents

-   **`ticket_analysis_agent`**:
    -   **Responsibility:** The first agent in the workflow. It receives the raw user query and performs an initial analysis, structuring the information into a `TicketAnalysis` object (urgency, category, sentiment, summary).
    -   **Output:** A raw JSON string that is then processed by the `update_ticket_after_analysis` tool.

-   **`knowledge_retrieval_agent`**:
    -   **Responsibility:** Searches the official ADK documentation, which has been ingested into a Vertex AI RAG Corpus.
    -   **Technology:** Uses the built-in `VertexAiRagRetrieval` tool from the ADK.
    -   **Output:** A string containing the most relevant snippets from the documentation.

-   **`db_retrieval_agent`**:
    -   **Responsibility:** Searches a BigQuery database of previously resolved tickets to find historical solutions to similar problems.
    -   **Technology:** Uses the custom `search_resolved_tickets_db` tool.
    -   **Output:** A string representation of a list of similar tickets found.

-   **`problem_solver_agent`**:
    -   **Responsibility:** One of the final "output" agents. It synthesizes all the context gathered by the previous agents (ticket analysis, KB results, DB results) to provide a comprehensive, text-based solution. It is designed for troubleshooting, configuration, and conceptual questions.
    -   **Output:** A professional, formatted text response for the end-user, including a disclaimer.

-   **`code_generator_agent`**:
    -   **Responsibility:** The other final "output" agent. It is activated when the ticket category is "Code Generation". It synthesizes all context to generate complete, high-quality code examples and applications.
    -   **Output:** A professional response that includes a full code block, an explanation, and a disclaimer.