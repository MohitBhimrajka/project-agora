# FILE: intelligent_support_triage/agent.py

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
# CORRECTED IMPORT: Use InvocationContext for the callback's type hint
from google.adk.agents.invocation_context import InvocationContext
from .prompts import ORCHESTRATOR_PROMPT
from .tools import create_ticket

# Import all sub-agents
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent
from .sub_agents.db_retrieval.agent import db_retrieval_agent

# CORRECTED FUNCTION SIGNATURE
# The parameter name MUST be `callback_context`. The type is InvocationContext.
def initialize_workflow_state(callback_context: InvocationContext):
    """
    Initializes required keys in the session state at the start of a turn
    to prevent KeyErrors during prompt formatting.
    """
    if "ticket" not in callback_context.state:
        callback_context.state["ticket"] = "{}" # Initialize as empty JSON string
    if "ticket_analysis" not in callback_context.state:
        callback_context.state["ticket_analysis"] = "{}" # Initialize as empty JSON string
    if "kb_retrieval_results" not in callback_context.state:
        callback_context.state["kb_retrieval_results"] = "Not run."
    if "db_retrieval_results" not in callback_context.state:
        callback_context.state["db_retrieval_results"] = "Not run."

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06",
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        create_ticket,
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent),
        AgentTool(solution_generation_agent),
    ],
    before_agent_callback=initialize_workflow_state,
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent