from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompts import ORCHESTRATOR_PROMPT
from .tools import create_ticket

# Import all sub-agents
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.db_retrieval.agent import db_retrieval_agent
from .sub_agents.problem_solver.agent import problem_solver_agent
from .sub_agents.code_generator.agent import code_generator_agent

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-05-06", # Use Pro for complex routing and reasoning
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        # These are now the building blocks the orchestrator can choose from.
        create_ticket,
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent),
        AgentTool(problem_solver_agent),
        AgentTool(code_generator_agent),
    ],
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent