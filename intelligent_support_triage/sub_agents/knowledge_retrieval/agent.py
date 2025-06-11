# FILE: intelligent_support_triage/sub_agents/knowledge_retrieval/agent.py

from google.adk.agents import Agent
# Note: we are no longer importing google_search or the individual tools
from intelligent_support_triage.tools import find_relevant_information

knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction="""
        You are a Knowledge Retrieval Specialist. Your only goal is to find
        relevant information to help solve a customer's support ticket.

        You have one tool: `find_relevant_information`.
        
        You will be given a query containing the summary and category of the ticket.
        You MUST call the `find_relevant_information` tool with this query.
        
        Return the exact output from the tool.
    """,
    tools=[
        find_relevant_information,
    ],
)