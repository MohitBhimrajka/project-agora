# FILE: project_agora/sub_agents/problem_solver/agent.py

"""Defines the Problem Solver Agent, which synthesizes context to provide solutions."""

from google.adk.agents import LlmAgent
from .prompts import PROBLEM_SOLVER_PROMPT

problem_solver_agent = LlmAgent(
    name="problem_solver_agent",
    model="gemini-2.5-pro",
    instruction=PROBLEM_SOLVER_PROMPT,
)
