# FILE: intelligent_support_triage/agent.py

from google.adk.agents import Agent
from .prompts import ORCHESTRATOR_PROMPT
from .tools import create_ticket # Import the new tool

# Sub-agent imports
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction=ORCHESTRATOR_PROMPT,
    # Add the regular tool alongside the sub-agents
    tools=[
        create_ticket,
    ],
    sub_agents=[
        ticket_analysis_agent,
        knowledge_retrieval_agent,
        solution_generation_agent,
    ],
    # The callback is no longer needed.
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent