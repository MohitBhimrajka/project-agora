# FILE: adk_copilot/sub_agents/knowledge_retrieval/agent.py

import os
from google.adk.agents import Agent
from google.adk.tools.retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# Load the corpus name from the environment variable
RAG_CORPUS_RESOURCE_NAME = "projects/agentops-dev/locations/us-central1/ragCorpora/8207810320882728960"

# The VertexAiRagRetrieval tool is a high-level tool that handles retrieval.
# The `query` parameter of this tool is what will be sent to the RAG engine.
search_knowledge_base = VertexAiRagRetrieval(
    name="search_knowledge_base",
    description="Searches the ADK knowledge base for a given developer query.",
    rag_resources=[
        rag.RagResource(rag_corpus=RAG_CORPUS_RESOURCE_NAME)
    ],
    similarity_top_k=5,
    vector_distance_threshold=0.5,
)

# This agent's only job is to expose the search_knowledge_base tool.
# It doesn't need complex prompting, as the orchestrator is already passing it a refined summary.
knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction="""
        You are a search specialist. Your only job is to execute a search
        for the given user request using the `search_knowledge_base` tool.
        You MUST call this tool with the user's verbatim request.
        Do not add any conversational text or attempt to rephrase the query.
    """,
    tools=[
        search_knowledge_base,
    ],
    output_key="kb_retrieval_results"
)