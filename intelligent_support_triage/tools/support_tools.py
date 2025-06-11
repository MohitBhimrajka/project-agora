# FILE: intelligent_support_triage/tools/support_tools.py

import os
from google.adk.tools import ToolContext
from google.cloud import bigquery
from vertexai import rag
from intelligent_support_triage.entities.ticket import SupportTicket

# --- Helper Functions (Internal to this module) ---

def _get_bq_client():
    project_id = os.getenv("BQ_PROJECT_ID")
    if not project_id:
        raise ValueError("BQ_PROJECT_ID environment variable not set.")
    return bigquery.Client(project=project_id)

def _search_knowledge_base(query: str) -> str:
    """Internal function to search the RAG-based knowledge base."""
    print(f"INFO: Searching knowledge base for: {query}")
    corpus_name = os.getenv("RAG_CORPUS_NAME")
    if not corpus_name:
        return "Configuration Error: RAG_CORPUS_NAME is not set. Cannot search knowledge base."

    try:
        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
            text=query,
            # Let's get more results to choose from
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=3)
        )
        # Format the response to be more readable for the LLM
        formatted_docs = [f"Doc: {ctx.text}" for ctx in response.contexts]
        return "\n---\n".join(formatted_docs) if formatted_docs else "No relevant documents found in the knowledge base."
    except Exception as e:
        return f"An error occurred during RAG retrieval: {str(e)}"

def _search_resolved_tickets_db(query: str) -> str:
    """Internal function to search historical tickets in BigQuery."""
    print(f"INFO: Searching resolved tickets DB with query: {query}")
    project_id = os.getenv("BQ_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID")

    if not all([project_id, dataset_id]):
        return "Configuration Error: BQ_PROJECT_ID or BQ_DATASET_ID is not set."

    # Use parameterized queries to prevent SQL injection
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("query_term", "STRING", f"%{query}%")
        ]
    )
    sql_query = f"""
        SELECT
            request,
            suggested_solution
        FROM
            `{project_id}.{dataset_id}.resolved_tickets`
        WHERE
            LOWER(request) LIKE LOWER(@query_term)
        LIMIT 3
    """

    try:
        client = _get_bq_client()
        query_job = client.query(sql_query, job_config=job_config)
        results = query_job.result()
        
        if results.total_rows == 0:
            return "No similar resolved tickets found in the database."

        formatted_results = [
            f"Similar Request: {row.request}\nProvided Solution: {row.suggested_solution}"
            for row in results
        ]
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"An error occurred while querying BigQuery: {str(e)}"

# --- The Main Tool for the Agent ---

def find_relevant_information(query: str, tool_context: ToolContext) -> str:
    """
    Searches internal knowledge sources to find relevant information for a
    customer support query. It first searches the official knowledge base,
    and if no conclusive results are found, it then searches the database of
    previously resolved tickets.

    Args:
        query: A natural language description of the customer's issue.
    
    Returns:
        A string containing the most relevant information found.
    """
    print(f"INFO: Finding relevant information for query: '{query}'")
    
    # 1. Search the official knowledge base first.
    kb_results = _search_knowledge_base(query)
    
    # 2. If the KB search wasn't conclusive, search past tickets.
    # We can define "not conclusive" as getting the default "not found" message.
    if "No relevant documents found" in kb_results:
        print("INFO: Knowledge base inconclusive. Searching resolved tickets database.")
        db_results = _search_resolved_tickets_db(query)
        # Combine results, prioritizing the DB results now.
        return f"Knowledge Base Results:\n{kb_results}\n\nResolved Ticket Results:\n{db_results}"
    
    # 3. If the KB had results, return them as they are the primary source.
    return f"Knowledge Base Results:\n{kb_results}"

# We still need this for the `create_ticket` tool
def create_ticket(request: str, tool_context: ToolContext) -> str:
    """
    Creates a new support ticket object from the user's initial request
    and saves it to the session state.
    """
    print(f"INFO: Creating a new ticket for request: '{request}'")
    ticket = SupportTicket(
        ticket_id="TICK-DEMO-001",
        customer_id="CUST-DEMO-123",
        request=request,
    )
    ticket_json = ticket.to_json()
    tool_context.state["ticket"] = ticket_json
    return ticket_json