# FILE: intelligent_support_triage/agent.py

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompts import ORCHESTRATOR_PROMPT
from .tools import create_ticket

# Import all sub-agents
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent
from .sub_agents.db_retrieval.agent import db_retrieval_agent # Import new agent

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06", # Using Pro model for more complex reasoning
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        create_ticket,
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent), # Add new agent to tool list
        AgentTool(solution_generation_agent),
    ],
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent