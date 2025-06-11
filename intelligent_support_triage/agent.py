import json
from google.adk.agents import Agent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools.agent_tool import AgentTool
from .prompts import ORCHESTRATOR_PROMPT
from .entities.ticket import SupportTicket

# ... (Import all sub-agents as before) ...
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.db_retrieval.agent import db_retrieval_agent
from .sub_agents.problem_solver.agent import problem_solver_agent
from .sub_agents.code_generator.agent import code_generator_agent

def initialize_workflow_state(ctx: InvocationContext):
    """
    Initializes or loads the support ticket at the start of a turn.
    """
    if "ticket" not in ctx.state or ctx.state["ticket"] == "{}":
        user_query = ""
        if ctx.conversation_history:
            user_query = ctx.conversation_history[-1].content.parts[0].text
        
        ticket = SupportTicket(
            ticket_id="TICK-DEMO-001",
            customer_id="CUST-DEMO-123",
            request=user_query,
            status="New"
        )
        ctx.state["ticket"] = ticket.to_json()
        print("INFO: New ticket created and state initialized.")

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-1.5-pro-preview-0514",
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent),
        AgentTool(problem_solver_agent),
        AgentTool(code_generator_agent),
    ],
    before_agent_callback=initialize_workflow_state,
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent