# FILE: project_agora/sub_agents/db_retrieval/agent.py

"""Defines the Database Retrieval Agent for searching historical tickets."""

from google.adk.agents import Agent

from ...tools import search_resolved_tickets_db
from .prompts import DB_RETRIEVAL_PROMPT

# This agent's only job is to execute the database search tool.
db_retrieval_agent = Agent(
    name="db_retrieval_agent",
    model="gemini-2.5-pro",
    instruction=DB_RETRIEVAL_PROMPT,
    tools=[
        search_resolved_tickets_db,
    ],
    # The output of the tool will be automatically saved to this state key.
    output_key="db_retrieval_results",
)
