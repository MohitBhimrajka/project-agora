# Tools Directory

This directory contains custom Python functions exposed as "tools" to the agent framework. These tools provide the agents with concrete capabilities, such as interacting with databases, generating images, or managing the application's state.

| Tool Function                      | Purpose                                                                                                        | Called By                 |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `create_ticket()`                    | The "intake" tool for the entire workflow. Creates the initial `SupportTicket` object in the session state.    | `orchestrator_agent`      |
| `update_ticket_after_analysis()`   | A state-management tool. It parses the JSON from the analysis agent and updates the ticket's status to "Analyzing". | `orchestrator_agent`      |
| `update_ticket_after_retrieval()`  | A state-management tool. It stores the results from the retrieval agents and updates the ticket's status to "AwaitingContextConfirmation". | `orchestrator_agent`      |
| `search_resolved_tickets_db()`     | Performs a semantic vector search on the Google BigQuery database of historical tickets.                         | `db_retrieval_agent`      |
| `read_user_file()`                 | Reads the text content of a user-provided file from a Google Cloud Storage URI.                                | `ticket_analysis_agent`   |
| `generate_diagram_from_mermaid()`  | Renders Mermaid syntax into a PNG image, uploads it to GCS, and returns a public URL.                          | `orchestrator_agent`      |