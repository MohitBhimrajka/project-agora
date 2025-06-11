# FILE: intelligent_support_triage/sub_agents/ticket_analysis/agent.py

from google.adk.agents import Agent
from google.adk.tools import ToolContext # Import ToolContext

# This is a specialized agent that uses a targeted prompt
# to perform a specific task and return a structured JSON string.
ticket_analysis_agent = Agent(
    name="ticket_analysis_agent",
    model="gemini-2.0-flash-001",
    instruction="""
        You are a support ticket analyst. Your task is to carefully read the
        provided ticket request and return a structured JSON object with your
        analysis.

        The JSON object must conform to the following schema:
        - "urgency": (string) How critical is this issue? (e.g., "Low", "Medium", "High")
        - "category": (string) What is the topic of the request? (e.g., "Technical", "Billing", "General Inquiry", "Password Reset", "API Integration", "Account Suspension")
        - "sentiment": (string) What is the emotional tone of the customer? (e.g., "Positive", "Neutral", "Negative", "Frustrated")
        - "summary": (string) Provide a concise, one-sentence summary of the customer's core issue.

        Analyze the user's request and provide ONLY the raw JSON object in your response. Do not include markdown fences like ```json or any other explanatory text.
    """,
    # Add an output_key to automatically save the raw JSON output to the state.
    output_key="ticket_analysis"
)