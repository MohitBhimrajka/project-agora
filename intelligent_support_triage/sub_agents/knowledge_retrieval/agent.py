# FILE: intelligent_support_triage/sub_agents/knowledge_retrieval/agent.py

import os
from google.adk.agents import Agent
from google.adk.tools.retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# This tool is now the ONLY tool for this agent.
search_knowledge_base = VertexAiRagRetrieval(
    name="search_knowledge_base",
    description="Searches official company documentation, FAQs, and guides. Use this for general 'how-to' questions or to understand features.",
    rag_resources=[
        rag.RagResource(rag_corpus=os.getenv("RAG_CORPUS_NAME"))
    ],
)

knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction="""
        You are a knowledge base specialist. You will be given a query
        summarizing a customer issue. Your only job is to call the
        `search_knowledge_base` tool with that exact query to find an
        official solution.
    """,
    tools=[
        search_knowledge_base,
    ],
)