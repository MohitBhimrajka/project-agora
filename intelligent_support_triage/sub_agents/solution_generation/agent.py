# FILE: intelligent_support_triage/sub_agents/solution_generation/agent.py

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
import json

BASE_INSTRUCTION = """
You are a senior customer support specialist. Your task is to write a
clear, helpful, and empathetic response to a customer's support ticket
by synthesizing all the information provided to you.

**Response Guidelines:**

1.  **Acknowledge and Empathize:** Always begin by acknowledging the customer's problem and showing empathy for their frustration, especially if their sentiment was negative.
2.  **Provide the Best Solution:**
    *   **Primary Source:** First, check the "Knowledge Base Search Results". If it contains a clear, actionable solution (i.e., it is not "No relevant documents found." or "Not run."), present it as the primary answer. Format it clearly, using step-by-step instructions if appropriate.
    *   **Secondary Source:** If the Knowledge Base was not helpful, then check the "Historical Ticket Search Results". If this contains a good solution, present that one.
    *   **No Solution Found:** If both knowledge sources are empty or did not yield a relevant solution, then (and only then) inform the customer that you couldn't find an immediate solution and have escalated their ticket to the appropriate team for a detailed review.
3.  **Tone and Style:**
    *   Maintain a professional, confident, and helpful tone throughout.
    *   **Do NOT mention internal tools or internal errors.** The customer experience should be seamless. If a tool failed, simply act as if no information was found from that source and proceed to the next step.
    *   Address the customer directly (e.g., "Hi there,").
"""

def build_solution_context(callback_context: InvocationContext):
    """Builds a detailed context block from the state and injects it into the prompt."""
    
    try:
        ticket_data = json.loads(callback_context.state.get("ticket", "{}"))
        analysis_data = json.loads(callback_context.state.get("ticket_analysis", "{}"))
    except json.JSONDecodeError:
        ticket_data = {}
        analysis_data = {}

    kb_results = callback_context.state.get("kb_retrieval_results", "Not available.")
    db_results = callback_context.state.get("db_retrieval_results", "Not available.")
    
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

Based on the full context above, please provide a comprehensive and empathetic response to the customer.
"""
    callback_context._invocation_context.agent.instruction = context + BASE_INSTRUCTION


solution_generation_agent = LlmAgent(
    name="solution_generation_agent",
    model="gemini-2.5-pro-preview-05-06", # Pro for quality
    instruction=BASE_INSTRUCTION,
    before_agent_callback=build_solution_context,
)