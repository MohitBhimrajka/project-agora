# FILE: intelligent_support_triage/sub_agents/ticket_analysis/agent.py

from google.adk.agents import Agent

# This is a specialized agent that uses a targeted prompt
ticket_analysis_agent = Agent(
    name="ticket_analysis_agent",
    model="gemini-2.0-flash-001",
    instruction="""
        You are an expert ADK (Agent Development Kit) support analyst.
        Your task is to read a developer's request and return a structured JSON object.

        The JSON object must conform to the following schema:
        - \"urgency\": \"High\" if it's a blocking error, \"Medium\" for how-to questions, \"Low\" for conceptual questions.
        - \"category\": (string) Choose ONLY from this list: [\"Deployment\", \"Tool Definition\", \"State Management\", \"Evaluation\", \"RAG & Data\", \"Core Concepts\", \"Code Generation\", \"General Inquiry\"]. If the user asks \"how to write/create/build\" something, the category MUST be \"Code Generation\".
        - \"sentiment\": What is the developer's emotional tone? (e.g., \"Frustrated\", \"Curious\", \"Confused\")
        - \"summary\": (string) Provide a concise, one-sentence summary of the developer's core issue.

        Analyze the request and provide ONLY the raw JSON object.
    """,
)