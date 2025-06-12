# Sub-Agents Directory

This directory contains the specialized "worker" agents managed by the main `orchestrator_agent`. Each sub-agent is a modular component with a single, well-defined responsibility in the developer support workflow. This separation of concerns is a core design principle of the ADK Copilot.

---

## Agent Profiles

### 1. `ticket_analysis_agent`
*   **Responsibility:** The first agent in the workflow. It performs initial triage on the raw user query.
*   **Input:** The developer's verbatim request (string).
*   **Output:** A structured JSON object containing `urgency`, `category`, `sentiment`, and `summary`.
*   **Key Technology:** `gemini-1.5-flash` with a strict JSON output prompt.

### 2. `knowledge_retrieval_agent`
*   **Responsibility:** Searches the official ADK documentation for relevant guides, APIs, and best practices.
*   **Input:** The summary of the issue from the ticket analysis.
*   **Output:** A string containing the most relevant snippets from the documentation.
*   **Key Technology:** The ADK's built-in `VertexAiRagRetrieval` tool connected to our RAG corpus.

### 3. `db_retrieval_agent`
*   **Responsibility:** Searches for historical solutions to similar problems in our BigQuery database.
*   **Input:** The summary of the issue from the ticket analysis.
*   **Output:** A string representation of similar past tickets found via vector search.
*   **Key Technology:** A custom tool (`search_resolved_tickets_db`) that executes a `COSINE_DISTANCE` vector search query in Google BigQuery.

### 4. `problem_solver_agent`
*   **Responsibility:** The final "synthesis" agent for providing text-based solutions. It is designed for troubleshooting, configuration, and conceptual questions.
*   **Input:** A comprehensive context block containing the original request, ticket analysis, and all retrieved data (from RAG and BigQuery).
*   **Output:** A professional, formatted Markdown response for the end-user.
*   **Key Technology:** `gemini-1.5-pro` with a detailed persona and response-formatting prompt.

### 5. `code_generator_agent`
*   **Responsibility:** The final "synthesis" agent for generating code. It is activated when the ticket category is "Code Generation".
*   **Input:** A comprehensive context block, identical to the problem solver's input.
*   **Output:** A multi-file ADK project, including code blocks, file paths, and setup instructions.
*   **Key Technology:** `gemini-1.5-pro` with a two-step (propose, then code) reasoning prompt to ensure accuracy.