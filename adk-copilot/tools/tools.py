# FILE: adk_copilot/tools/tools.py

import os
import json
from google.cloud import bigquery
from google.adk.tools import ToolContext
from ..entities.ticket import SupportTicket, TicketAnalysis
from difflib import SequenceMatcher

def _get_similarity(a: str, b: str) -> float:
    """Helper function to get a similarity score between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def create_ticket(request: str, tool_context: ToolContext) -> str:
    """
    Creates a new developer request and initializes the workflow state.
    This should be the very first tool called for any new developer request.
    
    Args:
        request: The user's original, verbatim developer request.
        tool_context: The context object provided by the ADK framework.

    Returns:
        A JSON string representing the newly created request.
    """
    ticket = SupportTicket(
        ticket_id="TICK-DEMO-001",
        customer_id="DEV-DEMO-123",
        request=request,
        status="New"  # The initial status
    )
    
    # Save the new request to the session state
    ticket_json = ticket.to_json()
    tool_context.state["ticket"] = ticket_json
    
    print("INFO: New developer request created via tool and state initialized.")
    return ticket_json


def search_resolved_tickets_db(query: str) -> str:
    """
    Searches the BigQuery database of resolved developer requests for entries matching a query.
    Only returns requests with a high similarity score to the query.

    Args:
        query: A string containing keywords to search for in past developer requests.

    Returns:
        A string representation of a list of matching requests, or an empty list if none are found.
    """
    bq_project_id = os.getenv("BQ_PROJECT_ID")
    bq_dataset_id = os.getenv("BQ_DATASET_ID")

    if not bq_project_id or not bq_dataset_id:
        return "Error: BigQuery project ID or dataset ID is not configured."

    client = bigquery.Client(project=bq_project_id)
    table_id = f"{bq_project_id}.{bq_dataset_id}.resolved_tickets"
    
    # A broader search to get more candidates to filter locally
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("search_query", "STRING", f"%{query.split()[0]}%") # Search for first word
        ]
    )
    
    # We remove the `request` column from the WHERE clause to avoid the previous error
    sql_query = f"""
        SELECT
            ticket_id,
            request,
            category,
            suggested_solution
        FROM
            `{table_id}` AS t
        WHERE
            LOWER(t.suggested_solution) LIKE LOWER(@search_query)
        LIMIT 20
    """

    try:
        print(f"INFO: Executing BigQuery search for candidates matching: '{query}'")
        query_job = client.query(sql_query, job_config=job_config)
        all_results = [dict(row) for row in query_job.result()]
        
        # Filter results based on a similarity threshold
        highly_relevant_requests = []
        for request in all_results:
            # Check similarity against both the request and solution for relevance
            request_similarity = _get_similarity(query, request.get("request", ""))
            solution_similarity = _get_similarity(query, request.get("suggested_solution", ""))
            
            # Use the higher of the two scores
            confidence = max(request_similarity, solution_similarity)
            
            # Only include if confidence is high enough (e.g., > 40%)
            if confidence > 0.4:
                highly_relevant_requests.append(request)
        
        if not highly_relevant_requests:
            return "[]" 

        return str(highly_relevant_requests)

    except Exception as e:
        print(f"ERROR: BigQuery search failed: {e}")
        return f"Error: Failed to execute database search. Details: {e}"

def update_ticket_after_analysis(analysis_json: str, tool_context: ToolContext) -> str:
    """
    Parses the analysis JSON, updates the main request object in the state
    with the analysis details, and sets the request status to 'Analyzing'.
    This tool should be called immediately after the ticket_analysis_agent runs.

    Args:
        analysis_json: The raw JSON string output from the ticket_analysis_agent.
        tool_context: The context object to access and modify the state.

    Returns:
        The updated request as a JSON string, or an error message.
    """
    try:
        # 1. Clean up the JSON string from markdown fences
        if analysis_json.strip().startswith("```json"):
            analysis_json = analysis_json.strip()[7:-4].strip()

        # 2. Load current request from state
        ticket_dict = json.loads(tool_context.state.get("ticket", "{}"))
        if not ticket_dict:
            return "Error: Request not found in state."

        # 3. Parse the new analysis data
        analysis_data = json.loads(analysis_json)
        
        # 4. Update the request object
        ticket_dict["analysis"] = TicketAnalysis(**analysis_data).model_dump()
        ticket_dict["status"] = "Analyzing"  # <-- CRITICAL: Update the status!

        # 5. Save the updated request back to the state
        updated_ticket_json = json.dumps(ticket_dict, indent=2)
        tool_context.state["ticket"] = updated_ticket_json

        print(f"INFO: Request status updated to 'Analyzing'. Analysis: {analysis_data}")
        return updated_ticket_json

    except (json.JSONDecodeError, KeyError) as e:
        error_msg = f"Error processing analysis and updating request: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg