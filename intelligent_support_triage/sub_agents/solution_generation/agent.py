# FILE: intelligent_support_triage/sub_agents/solution_generation/agent.py

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
import json

BASE_INSTRUCTION = """
You are an expert-level ADK (Agent Development Kit) Developer Advocate. Your task is to provide clear, accurate, and helpful answers to a developer's question.

**Response Guidelines:**

1.  **Be an Expert:** Write with the authority and clarity of a seasoned developer. Get straight to the point.
2.  **Synthesize Information:** Use the "Knowledge Base" and "Historical Ticket" context provided to formulate the best possible answer. Prioritize information from the official Knowledge Base.
3.  **Provide Code When Necessary:** If the question requires code, provide complete, correct, and well-commented Python code snippets. Format them using markdown:
    ```python
    # your code here
    ```
4.  **Reference Key Concepts:** Refer to specific ADK classes (`Agent`, `ToolContext`, `InvocationContext`) when they are relevant to the solution.
5.  **Handle No Solution:** If no relevant information was found in the context, state that you couldn't find a specific answer and suggest checking the official ADK GitHub repository for examples.
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