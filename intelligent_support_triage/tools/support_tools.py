# FILE: intelligent_support_triage/tools/support_tools.py

import os
import json
from google.adk.tools import ToolContext
from google.cloud import bigquery
from intelligent_support_triage.entities.ticket import SupportTicket

def search_resolved_tickets_db(query: str, tool_context: ToolContext) -> str:
    """
    Searches a database of previously resolved support tickets for similar issues.
    Use this to find solutions for common, recurring problems.
    """
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
    
    # FINAL FIX: Use a table alias `t` to prevent ambiguity.
    sql_query = f"""
        SELECT
            t.request,
            t.suggested_solution
        FROM
            `{project_id}.{dataset_id}.resolved_tickets` AS t
        WHERE
            LOWER(t.request) LIKE LOWER(@query_term)
        LIMIT 3
    """

    try:
        client = bigquery.Client(project=project_id)
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

def create_ticket(request: str, tool_context: ToolContext) -> str:
    """
    Creates a new support ticket object from the user's initial request
    and saves it to the session state. This should be the first step for any new support issue.
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