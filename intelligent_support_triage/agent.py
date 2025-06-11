# FILE: intelligent_support_triage/agent.py

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool # <-- IMPORT THIS
from .prompts import ORCHESTRATOR_PROMPT
from .tools import create_ticket

# Sub-agent imports
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction=ORCHESTRATOR_PROMPT,
    # UNIFY all actions into a single `tools` list.
    # Sub-agents are wrapped in `AgentTool`.
    tools=[
        create_ticket,
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(solution_generation_agent),
    ],
    # REMOVED the separate `sub_agents` parameter.
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent