# FILE: project_agora/agent.py

"""
Defines the main Orchestrator Agent for Project Agora.
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
    update_ticket_after_retrieval,
    generate_diagram_from_mermaid,
    format_code_reviewer_output,
)

from .callbacks import before_agent_call, before_tool_call, after_tool_call

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro",
    global_instruction="""
        You are 'Agora', the central orchestrator for a team of autonomous AI agents.
        Your goal is to manage your specialist agents to provide accurate, helpful, and professional support to developers.
        Always interact in a friendly and professional tone.
    """,
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        create_ticket,
        update_ticket_after_analysis,
        update_ticket_after_retrieval,
        generate_diagram_from_mermaid,
        format_code_reviewer_output,
        AgentTool(ticket_analysis_agent),
        AgentTool(knowledge_retrieval_agent),
        AgentTool(db_retrieval_agent),
        AgentTool(problem_solver_agent),
        AgentTool(code_generator_agent),
        AgentTool(code_reviewer_agent),
    ],
    before_agent_callback=before_agent_call,
    before_tool_callback=before_tool_call,
    after_tool_callback=after_tool_call,
)

root_agent = orchestrator_agent