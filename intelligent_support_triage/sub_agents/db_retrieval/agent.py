# FILE: intelligent_support_triage/sub_agents/db_retrieval/agent.py

from google.adk.agents import Agent
from intelligent_support_triage.tools import search_resolved_tickets_db

# This agent has one job: search the database of past tickets.
db_retrieval_agent = Agent(
    name="db_retrieval_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction="""
        You are a database retrieval specialist. You will be given a query
        summarizing a customer issue. Your only job is to call the
        `search_resolved_tickets_db` tool with that exact query to find
        similar past tickets.
    """,
    tools=[
        search_resolved_tickets_db,
    ],
)