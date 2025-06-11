# FILE: intelligent_support_triage/sub_agents/db_retrieval/agent.py

from google.adk.agents import Agent  # <-- Use the base Agent
from ...tools import search_resolved_tickets_db

# This agent's only job is to execute the database search tool.
db_retrieval_agent = Agent(
    name="db_retrieval_agent",
    model="gemini-2.0-flash-001",
    instruction="You are a specialist whose only purpose is to search a database of past support tickets. You will be given a query. You MUST use the `search_resolved_tickets_db` tool to find similar past tickets.",
    tools=[
        search_resolved_tickets_db,
    ],
    # The output of the tool will be automatically saved to this state key.
    output_key="db_retrieval_results",
)