# Tools Directory

This directory contains custom Python functions exposed as "tools" to the agent framework. These tools provide the agents with concrete capabilities, such as interacting with databases or managing the application's state.

| Tool Function                      | Purpose                                                                                                        | Called By                 |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `create_ticket()`                    | The "intake" tool for the entire workflow. Creates the initial `SupportTicket` object in the session state.    | `orchestrator_agent`      |
| `update_ticket_after_analysis()`   | A crucial state-management tool. It parses the JSON from the analysis agent and updates the ticket's status. | `orchestrator_agent`      |
| `search_resolved_tickets_db()`     | Performs a semantic vector search on the Google BigQuery database of historical tickets.                         | `db_retrieval_agent`      |