from google.adk.agents import Agent
from intelligent_support_triage.entities.ticket import TicketAnalysis

# This is a specialized agent that uses a targeted prompt
# and a structured output (Pydantic model) to perform a specific task.
ticket_analysis_agent = Agent( # CORRECTED: Changed from LlmAgent to Agent
    name="ticket_analysis_agent",
    model="gemini-2.0-flash-001",
    # CORRECTED: The instruction now explicitly asks for a JSON output
    # that matches the structure of our TicketAnalysis Pydantic model.
    instruction=f"""
        You are a support ticket analyst. Your task is to carefully read the
        provided ticket request and return a structured JSON object with your
        analysis.

        The JSON object must conform to the following schema:
        - "urgency": (string) How critical is this issue? (e.g., "Low", "Medium", "High")
        - "category": (string) What is the topic of the request? (e.g., "Technical", "Billing", "General Inquiry", "Password Reset")
        - "sentiment": (string) What is the emotional tone of the customer? (e.g., "Positive", "Neutral", "Negative", "Frustrated")
        - "summary": (string) Provide a concise, one-sentence summary of the customer's core issue.

        Analyze the user's request and provide ONLY the raw JSON object in your response.
    """,
    # CORRECTED: Removed the invalid `response_model` parameter.
)