# FILE: project_agora/sub_agents/ticket_analysis/agent.py

"""Defines the Ticket Analysis Agent for initial request categorization."""

from google.adk.agents import Agent
from ...tools.file_reader_tool import read_user_file
from .prompts import TICKET_ANALYSIS_PROMPT

# This is a specialized agent that uses a targeted prompt
ticket_analysis_agent = Agent(
    name="ticket_analysis_agent",
    model="gemini-2.5-flash",
    instruction=TICKET_ANALYSIS_PROMPT,
    tools=[read_user_file],
)
