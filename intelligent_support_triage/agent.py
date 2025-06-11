# FILE: intelligent_support_triage/agent.py

import json
from google.adk.agents import Agent
from .prompts import ORCHESTRATOR_PROMPT
from .entities.ticket import SupportTicket

# Sub-agent imports remain the same
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent

# The main Orchestrator Agent
# REMOVED the before_agent_callback. The LLM will now handle the workflow.
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06", # Using a more capable model for orchestration
    instruction=ORCHESTRATOR_PROMPT,
    sub_agents=[
        ticket_analysis_agent,
        knowledge_retrieval_agent,
        solution_generation_agent,
    ],
    # By providing the SupportTicket model here, we can initialize it in the state.
    state_model=SupportTicket
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent