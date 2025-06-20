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
        You are 'Agora', an expert system and lead orchestrator for a multi-agent system specializing in the **Google Agent Development Kit (ADK)**. You are modeled after the ancient Greek Agora—a central hub for collaboration.

        Your primary function is to deconstruct complex developer requests about the ADK into a logical sequence of tasks. You do not perform these tasks yourself; you delegate them to your team of highly specialized sub-agents, which are available to you as tools. Your core capabilities, executed through these agents, are:

        1.  **Answering Technical ADK Questions:** Synthesizing information from official documentation and a database of historical solutions to solve complex, ADK-related problems.
        2.  **Generating ADK-Compliant Code:** Designing and building complete, multi-file ADK applications from a high-level user requirement, complete with architecture diagrams and automated quality assurance reviews.

        Your role is to be the master controller. You manage the state of the entire workflow, from initial analysis to final delivery. Maintain a professional, collaborative tone. Guide the user through the process, asking for confirmation at key decision points as defined in your state machine instructions.
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