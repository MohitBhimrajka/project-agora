# FILE: adk_copilot/tools/tools.py

import json
import os
import uuid

from google.adk.tools import ToolContext
from google.cloud import bigquery
from vertexai.language_models import TextEmbeddingModel

from ..entities.ticket import SupportTicket, TicketAnalysis


def _get_embedding_for_query(
    text: str, model_name: str = "text-embedding-004"
) -> list[float]:
    """Helper function to generate an embedding for the user's query."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    try:
        embeddings = model.get_embeddings([text])
        return embeddings[0].values
    except Exception as e:
        print(f"ERROR: Could not get embedding for query: {e}")
        return None


def create_ticket(request: str, tool_context: ToolContext) -> str:
    """Creates a new developer request and initializes the workflow state."""
    ticket = SupportTicket(
        ticket_id=f"TICK-{str(uuid.uuid4())[:8].upper()}",
        customer_id=f"DEV-{str(uuid.uuid4())[:8].upper()}",
        request=request,
        status="New",
    )
    ticket_json = ticket.to_json()
    tool_context.state["ticket"] = ticket_json
    print("INFO: New developer request created via tool and state initialized.")
    return ticket_json


def search_resolved_tickets_db(query: str) -> str:
    """Performs a semantic vector search on the BigQuery database of resolved tickets."""
    print(f"INFO: Starting semantic search for query: '{query}'")

    bq_project_id = os.getenv("BQ_PROJECT_ID")
    bq_dataset_id = os.getenv("BQ_DATASET_ID")

    if not bq_project_id or not bq_dataset_id:
        return "Error: BigQuery project ID or dataset ID is not configured."

    query_embedding = _get_embedding_for_query(query)
    if not query_embedding:
        return "Error: Could not generate an embedding for the search query."

    client = bigquery.Client(project=bq_project_id)
    table_id = f"{bq_project_id}.{bq_dataset_id}.resolved_tickets"

    sql_query = f"""
        SELECT
            ticket_id,
            request,
            category,
            suggested_solution,
            -- Calculate the cosine distance between the query vector and the stored embeddings
            COSINE_DISTANCE(request_embedding, @query_embedding) as distance
        FROM
            `{table_id}`
        -- Order by distance (smaller is better) and return the top 3 matches
        ORDER BY
            distance
        LIMIT 3
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("query_embedding", "FLOAT64", query_embedding),
        ]
    )

    try:
        print(f"INFO: Executing BigQuery vector search...")
        query_job = client.query(sql_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]

        if not results:
            return "[]"

        return str(results)

    except Exception as e:
        print(f"ERROR: BigQuery vector search failed: {e}")
        return f"Error: Failed to execute database vector search. Details: {e}"


def update_ticket_after_analysis(analysis_json: str, tool_context: ToolContext) -> str:
    """Parses the analysis JSON, updates the main request object in the state."""
    try:
        if analysis_json.strip().startswith("```json"):
            analysis_json = analysis_json.strip()[7:-4].strip()

        ticket_dict = json.loads(tool_context.state.get("ticket", "{}"))
        if not ticket_dict:
            return "Error: Request not found in state."

        analysis_data = json.loads(analysis_json)

        ticket_dict["analysis"] = TicketAnalysis(**analysis_data).model_dump()
        ticket_dict["status"] = "Analyzing"

        updated_ticket_json = json.dumps(ticket_dict, indent=2)
        tool_context.state["ticket"] = updated_ticket_json

        print(f"INFO: Request status updated to 'Analyzing'. Analysis: {analysis_data}")
        return updated_ticket_json

    except (json.JSONDecodeError, KeyError) as e:
        error_msg = f"Error processing analysis and updating request: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg
