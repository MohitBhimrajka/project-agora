# FILE: intelligent_support_triage/tools/tools.py

import os
from google.cloud import bigquery
from google.adk.tools import ToolContext
from ..entities.ticket import SupportTicket
import json
from google.adk.tools.agent_tool import AgentTool
from ..sub_agents.problem_solver.agent import problem_solver_agent
from ..sub_agents.code_generator.agent import code_generator_agent

def search_resolved_tickets_db(query: str) -> str:
    """
    Searches the BigQuery database of resolved tickets for entries matching a query.

    Args:
        query: A string containing keywords to search for in past ticket requests.

    Returns:
        A string representation of a list of matching tickets, or an empty list if none are found.
    """
    bq_project_id = os.getenv("BQ_PROJECT_ID")
    bq_dataset_id = os.getenv("BQ_DATASET_ID")

    if not bq_project_id or not bq_dataset_id:
        return "Error: BigQuery project ID or dataset ID is not configured."

    client = bigquery.Client(project=bq_project_id)
    table_id = f"{bq_project_id}.{bq_dataset_id}.resolved_tickets"
    
    # Use query parameters to prevent SQL injection
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("search_query", "STRING", f"%{query}%")
        ]
    )

    # Note the aliasing (`AS t`) and use of `t.request` to prevent ambiguity errors.
    sql_query = f"""
        SELECT
            ticket_id,
            request,
            category,
            suggested_solution
        FROM
            `{table_id}` AS t
        WHERE
            LOWER(t.request) LIKE LOWER(@search_query) OR LOWER(t.suggested_solution) LIKE LOWER(@search_query)
        LIMIT 5
    """

    try:
        print(f"INFO: Executing BigQuery search for: '{query}'")
        query_job = client.query(sql_query, job_config=job_config)
        results = query_job.result()  # Waits for the job to complete.
        
        # Convert results to a list of dictionaries
        matching_tickets = [dict(row) for row in results]

        if not matching_tickets:
            return "[]" # Return an empty list as a string

        # Return the list of dictionaries as a string
        return str(matching_tickets)

    except Exception as e:
        print(f"ERROR: BigQuery search failed: {e}")
        return f"Error: Failed to execute database search. Details: {e}"
    
def create_ticket(request: str, tool_context: ToolContext) -> str:
    """
    Creates a new support ticket and initializes the workflow state.
    This should be the very first tool called for any new support request.
    
    Args:
        request: The user's original, verbatim support request.
        tool_context: The context object provided by the ADK framework.

    Returns:
        A JSON string representing the newly created ticket.
    """
    ticket = SupportTicket(
        ticket_id="TICK-DEMO-001",
        customer_id="CUST-DEMO-123",
        request=request,
        status="New"  # The initial status
    )
    
    # Save the new ticket to the session state
    ticket_json = ticket.to_json()
    tool_context.state["ticket"] = ticket_json
    
    print("INFO: New ticket created via tool and state initialized.")
    return ticket_json

async def build_and_delegate_solution(tool_context: ToolContext) -> str:
    """
    Assembles all context from the state and delegates to the correct final
    solution agent (problem_solver or code_generator) based on the analysis.
    This is the final step in the workflow.
    """
    try:
        # Load all necessary data from state
        ticket_data = json.loads(tool_context.state.get("ticket", "{}"))
        analysis_data = json.loads(tool_context.state.get("ticket_analysis", "{}"))
        kb_results = tool_context.state.get("kb_retrieval_results", "No KB results found.")
        db_results = tool_context.state.get("db_retrieval_results", "No similar historical tickets found.")
        
        # Build the comprehensive context string
        full_context = f"""
### FULL TICKET CONTEXT & TASK ###
You have been delegated a support ticket to resolve. Here is all the information gathered so far:

**Original Developer Request:**
{ticket_data.get('request', 'N/A')}

**Automated Analysis:**
- Urgency: {analysis_data.get('urgency', 'N/A')}
- Category: {analysis_data.get('category', 'N/A')}
- Sentiment: {analysis_data.get('sentiment', 'N/A')}
- Summary: {analysis_data.get('summary', 'N/A')}

**Retrieved from Knowledge Base:**
{kb_results}

**Retrieved from Historical Tickets:**
{db_results}

**Your Task:**
Based on all the context above, provide the final, comprehensive solution to the developer.
"""
        
        # Decide which agent to delegate to
        category = analysis_data.get("category")
        if category == "Code Generation Request":
            final_agent = code_generator_agent
        else:
            final_agent = problem_solver_agent
            
        print(f"INFO: Delegating to final agent: {final_agent.name}")
        
        # Use AgentTool to run the final agent with the full context
        agent_tool = AgentTool(agent=final_agent)
        final_solution = await agent_tool.run_async(
            args={"request": full_context}, tool_context=tool_context
        )
        
        return final_solution

    except (json.JSONDecodeError, KeyError) as e:
        error_msg = f"Error: Could not build final context due to missing or invalid state data. Details: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg