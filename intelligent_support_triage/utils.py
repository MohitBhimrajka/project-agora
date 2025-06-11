import json
from google.adk.agents.invocation_context import InvocationContext

def build_solution_context(ctx: InvocationContext):
    """Builds a detailed context block from the state and injects it into the prompt."""
    
    try:
        ticket_data = json.loads(ctx.state.get("ticket", "{}"))
        analysis_data = json.loads(ctx.state.get("ticket_analysis", "{}"))
    except json.JSONDecodeError:
        ticket_data = {}
        analysis_data = {}

    kb_results = ctx.state.get("kb_retrieval_results", "Not available.")
    db_results = ctx.state.get("db_retrieval_results", "Not available.")
    
    context_header = f"""
### FULL TICKET CONTEXT START ###
Original Request: {ticket_data.get('request', 'N/A')}

Ticket Analysis:
- Urgency: {analysis_data.get('urgency', 'N/A')}
- Category: {analysis_data.get('category', 'N/A')}
- Sentiment: {analysis_data.get('sentiment', 'N/A')}
- Summary: {analysis_data.get('summary', 'N/A')}

Knowledge Base Search Results:
{kb_results}

Historical Ticket Search Results:
{db_results}
### FULL TICKET CONTEXT END ###

Based on the full context above, please provide a comprehensive response to the developer.
"""
    # This dynamically updates the agent's instructions for this specific turn.
    base_instruction = ctx.agent.instruction
    ctx.agent.instruction = context_header + base_instruction