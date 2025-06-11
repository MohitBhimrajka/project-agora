# FILE: intelligent_support_triage/sub_agents/knowledge_retrieval/agent.py

import os
from google.adk.agents import Agent
from google.adk.tools.retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

search_knowledge_base = VertexAiRagRetrieval(
    name="search_knowledge_base",
    description="Searches the knowledge base for a given query.",
    rag_resources=[
        rag.RagResource(rag_corpus=os.getenv("RAG_CORPUS_NAME"))
    ],
    similarity_top_k=3,
    vector_distance_threshold=0.5,
)

knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.0-flash-001",
    instruction="""
        You are a search specialist. Your only job is to execute a search
        for the given user request using the `search_knowledge_base` tool.
        You must call this tool. Do not add any conversational text.
    """,
    tools=[
        search_knowledge_base,
    ],
    output_key="kb_retrieval_results"
)