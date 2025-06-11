# FILE: intelligent_support_triage/tools/support_tools.py

import os
import json
from google.adk.tools import ToolContext
from google.cloud import bigquery
# Corrected relative import
from ..entities.ticket import SupportTicket

def search_resolved_tickets_db(query: str, tool_context: ToolContext) -> str:
    """
    Searches a database of previously resolved support tickets for similar issues.
    """
    print(f"INFO: Searching resolved tickets DB with query: {query}")
    project_id = os.getenv("BQ_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID")

    if not all([project_id, dataset_id]):
        return "Configuration Error: BQ_PROJECT_ID or BQ_DATASET_ID is not set."

    # THIS IS THE DEFINITIVE, CORRECT SQL SYNTAX FOR PARAMETERIZED 'LIKE'
    sql_query = f"""
        SELECT
            t.request,
            t.suggested_solution
        FROM
            `{project_id}.{dataset_id}.resolved_tickets` AS t
        WHERE
            LOWER(t.request) LIKE @query_term OR LOWER(t.suggested_solution) LIKE @query_term
        LIMIT 3
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            # The parameter value ITSELF contains the wildcards.
            bigquery.ScalarQueryParameter("query_term", "STRING", f"%{query.lower()}%")
        ]
    )

    try:
        client = bigquery.Client(project=project_id)
        query_job = client.query(sql_query, job_config=job_config)
        results = query_job.result()
        
        if results.total_rows == 0:
            return "No similar resolved tickets found in the database."

        formatted_results = [
            f"Similar Request: {row.request}\\nProvided Solution: {row.suggested_solution}"
            for row in results
        ]
        return "\\n---\\n".join(formatted_results)
    except Exception as e:
        return f"Database Search Error: {str(e)}"

def create_ticket(request: str, tool_context: ToolContext) -> str:
    """
    Creates a new support ticket and initializes the state for the workflow.
    """
    print(f"INFO: Creating a new ticket for request: '{request}'")
    ticket = SupportTicket(
        ticket_id="TICK-DEMO-001",
        customer_id="CUST-DEMO-123",
        request=request,
    )
    ticket_json = ticket.to_json()
    
    print("INFO: Initializing workflow state.")
    tool_context.state["ticket"] = ticket_json
    tool_context.state["ticket_analysis"] = "{}"
    tool_context.state["kb_retrieval_results"] = "Not run."
    tool_context.state["db_retrieval_results"] = "Not run."
    
    return ticket_json