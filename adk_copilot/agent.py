# FILE: adk_copilot/agent.py

"""
Defines the main Orchestrator Agent for the ADK Copilot system.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .prompts import ORCHESTRATOR_PROMPT

# Import all sub-agents and tools
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.db_retrieval.agent import db_retrieval_agent
from .sub_agents.problem_solver.agent import problem_solver_agent
from .sub_agents.code_generator.agent import code_generator_agent
from .sub_agents.code_reviewer.agent import code_reviewer_agent

# Import tools that the orchestrator will call directly
from .tools.tools import (
    create_ticket,
    update_ticket_after_analysis,
    generate_diagram_from_mermaid,
)


# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro-preview-05-06",
    global_instruction="""
        You are 'ADK Copilot', an expert AI assistant for the Google Agent Development Kit.
        Your goal is to provide accurate, helpful, and professional support to developers.
        You manage a team of specialist agents to solve problems.
        Always interact in a friendly and professional tone.
    """,
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        # List ALL possible tools and sub-agents the orchestrator can call
        create_ticket,
        update_ticket_after_analysis,
        generate_diagram_from_mermaid,
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent),
        AgentTool(problem_solver_agent),
        AgentTool(code_generator_agent),
        AgentTool(code_reviewer_agent),
    ],
)

root_agent = orchestrator_agent