# FILE: intelligent_support_triage/sub_agents/knowledge_retrieval/agent.py

import os
from google.adk.agents import Agent
from google.adk.tools.retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from intelligent_support_triage.tools import search_resolved_tickets_db

# Use the ADK's built-in tool for RAG. It's more robust.
search_knowledge_base = VertexAiRagRetrieval(
    name="search_knowledge_base",
    description="Searches official company documentation, FAQs, and guides. Use this for general 'how-to' questions or to understand features.",
)

knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction="""
        You are a Knowledge Retrieval Specialist. Your goal is to find the most
        relevant information to solve a customer's support ticket using the tools provided.

        You have two tools:
        1.  `search_knowledge_base`: Use this for "how-to" questions, feature explanations, and official policies.
        2.  `search_resolved_tickets_db`: Use this to find solutions for specific error messages or recurring problems that might have been solved before.

        Analyze the user's query, which contains a summary of their problem.
        Choose the SINGLE most appropriate tool to find a solution. Return the
        information you find.
    """,
    tools=[
        search_knowledge_base,
        search_resolved_tickets_db,
    ],
)