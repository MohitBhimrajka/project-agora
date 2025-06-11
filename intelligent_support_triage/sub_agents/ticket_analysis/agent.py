from google.adk.agents import LlmAgent
from intelligent_support_triage.entities.ticket import TicketAnalysis

# This is a specialized agent that uses a targeted prompt
# and a structured output (Pydantic model) to perform a specific task.
ticket_analysis_agent = LlmAgent(
    name="ticket_analysis_agent",
    model="gemini-2.0-flash-001",
    instruction="""
        You are a support ticket analyst. Your task is to carefully read the
        provided ticket request and extract key information.

        Analyze the following aspects:
        - **Urgency:** How critical is this issue? (e.g., Low, Medium, High)
        - **Category:** What is the topic of the request? (e.g., Technical, Billing, General Inquiry, Password Reset)
        - **Sentiment:** What is the emotional tone of the customer? (e.g., Positive, Neutral, Negative, Frustrated)
        - **Summary:** Provide a concise, one-sentence summary of the customer's core issue.
    """,
    # By specifying a response_model, the agent will automatically
    # format its output into a structured JSON object matching the TicketAnalysis model.
    response_model=TicketAnalysis,
)