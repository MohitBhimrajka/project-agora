# Tools Directory

This directory contains custom Python functions that are exposed as "tools" to the agent framework. These tools provide the agents with concrete capabilities beyond simple text generation, such as interacting with databases or updating the session state.

### Tools

-   **`create_ticket(request: str, tool_context: ToolContext)`**:
    -   **Purpose:** The "intake" tool for the entire workflow. It takes the user's initial request and creates the initial `SupportTicket` object in the session state.
    -   **Called By:** `orchestrator_agent` as the very first step for any new support issue.

-   **`update_ticket_after_analysis(analysis_json: str, tool_context: ToolContext)`**:
    -   **Purpose:** A crucial state-management tool. It takes the raw JSON output from the `ticket_analysis_agent`, parses it, and formally updates the main `SupportTicket` object in the state.
    -   **Key Action:** It is responsible for transitioning the ticket's `status` from `"New"` to `"Analyzing"`, which allows the workflow to proceed to the next stage.
    -   **Called By:** `orchestrator_agent` immediately after the `ticket_analysis_agent` completes its task.

-   **`search_resolved_tickets_db(query: str)`**:
    -   **Purpose:** Interacts with the Google BigQuery backend. It searches the historical `resolved_tickets` table for issues similar to the current one.
    -   **Features:** Includes a simple confidence scoring mechanism (`difflib`) to filter for only the most relevant historical tickets, improving the quality of the context passed to the final solver agents.
    -   **Called By:** The specialized `db_retrieval_agent`.