from google.adk.agents import Agent
from google.adk.tools import google_search
from intelligent_support_triage.tools import search_knowledge_base, search_resolved_tickets_db

knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.5-pro-preview-05-06", # A more powerful model for reasoning about which tool to use
    instruction="""
        You are a Knowledge Retrieval Specialist. Your goal is to find the most
        relevant information to help solve a customer's support ticket.

        You have access to three tools:
        1. `search_knowledge_base`: Use this first to search official company
           documentation, FAQs, and guides.
        2. `search_resolved_tickets_db`: If the knowledge base yields no results,
           use this to see if a similar issue has been resolved before.
        3. `google_search`: If both internal sources fail, use this for general
           troubleshooting information from the web.

        Based on the ticket summary, decide which tool is most appropriate.
        Return the information you find. If you find information from multiple
        sources, synthesize it into a single, coherent response.
    """,
    tools=[
        search_knowledge_base,
        search_resolved_tickets_db,
        google_search,
    ],
)