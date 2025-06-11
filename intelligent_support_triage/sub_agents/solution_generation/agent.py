# FILE: intelligent_support_triage/sub_agents/solution_generation/agent.py

from google.adk.agents import LlmAgent
# Type hint can remain InvocationContext for clarity, but the access pattern is key.
from google.adk.agents.invocation_context import InvocationContext
import json

BASE_INSTRUCTION = """
You are a senior customer support specialist. Your task is to write a
clear, helpful, and empathetic response to a customer's support ticket.

You will be given the full context including:
1. The original ticket request.
2. A structured analysis of the ticket.
3. The results from searching the knowledge base and historical tickets.

Your goal is to synthesize all this information into a single, comprehensive solution.

**Guidelines for your response:**
- Address the customer directly and always acknowledge their issue with empathy, especially if their sentiment was negative or frustrated.
- **If the retrieved knowledge contains a clear solution:** Present it in a simple, step-by-step format.
- **If the retrieved knowledge contains an error message (e.g., "Configuration Error", "error occurred while querying BigQuery"):** Do NOT show this error to the customer. Instead, calmly state that you were unable to find an immediate solution and have escalated the ticket to the appropriate team for review. Mention that the ticket has been marked with the correct priority based on the analysis.
- **If the retrieved knowledge is empty or inconclusive ("No relevant documents found" or "Not run."):** Inform the customer that you couldn't find a ready-made solution in the knowledge base and have escalated their ticket for human review.
- Maintain a professional and helpful tone throughout.
- **Crucially, do not mention the internal tools or agents used.** The customer should only see a single, seamless response from the support team.
"""

# The parameter name must be callback_context.
def build_solution_context(callback_context: InvocationContext):
    """Builds a detailed context block from the state and injects it into the prompt."""
    
    # Safely load data from state
    try:
        ticket_data = json.loads(callback_context.state.get("ticket", "{}"))
        analysis_data = json.loads(callback_context.state.get("ticket_analysis", "{}"))
    except json.JSONDecodeError:
        ticket_data = {}
        analysis_data = {}

    kb_results = callback_context.state.get("kb_retrieval_results", "Not available.")
    db_results = callback_context.state.get("db_retrieval_results", "Not available.")
    
    # Build the context string
    context = f"""
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

Based on the context above, please provide a comprehensive and empathetic response to the customer.
"""
    # THIS IS THE FINAL, CORRECTED LINE
    # Access the agent through the _invocation_context attribute.
    callback_context._invocation_context.agent.instruction = context + BASE_INSTRUCTION


solution_generation_agent = LlmAgent(
    name="solution_generation_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction=BASE_INSTRUCTION,
    before_agent_callback=build_solution_context,
)