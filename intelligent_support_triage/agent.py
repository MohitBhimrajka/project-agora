# FILE: intelligent_support_triage/agent.py

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompts import ORCHESTRATOR_PROMPT
# Import the new builder tool and the intake tool
from .tools import create_ticket, build_and_delegate_solution

# Import only the agents that are called directly by the orchestrator
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.db_retrieval.agent import db_retrieval_agent

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        # The tool list is now much cleaner
        create_ticket,
        build_and_delegate_solution, # <-- NEW
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent),
        # problem_solver and code_generator are no longer called directly
    ],
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent