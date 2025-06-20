# FILE: project_agora/sub_agents/knowledge_retrieval/agent.py

"""Defines the Knowledge Retrieval Agent for RAG-based documentation search."""

import os

from google.adk.agents import Agent
from google.adk.tools.retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from .prompts import KNOWLEDGE_RETRIEVAL_PROMPT

# Load the corpus name from the environment variable
RAG_CORPUS_RESOURCE_NAME = os.getenv("RAG_CORPUS_NAME")

# The VertexAiRagRetrieval tool is a high-level tool that handles retrieval.
# The `query` parameter of this tool is what will be sent to the RAG engine.
search_knowledge_base = VertexAiRagRetrieval(
    name="search_knowledge_base",
    description="Searches the ADK knowledge base for a given developer query.",
    rag_resources=[rag.RagResource(rag_corpus=RAG_CORPUS_RESOURCE_NAME)],
    similarity_top_k=5,
    vector_distance_threshold=0.5,
)

# This agent's only job is to expose the search_knowledge_base tool.
knowledge_retrieval_agent = Agent(
    name="knowledge_retrieval_agent",
    model="gemini-2.5-pro",
    instruction=KNOWLEDGE_RETRIEVAL_PROMPT,
    tools=[
        search_knowledge_base,
    ],
    output_key="kb_retrieval_results",
)
