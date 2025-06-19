# FILE: adk_copilot/sub_agents/code_generator/agent.py

"""Defines the Code Generator Agent, responsible for creating code."""

from google.adk.agents import LlmAgent
from .prompts import CODE_GENERATOR_PROMPT

# The agent instantiation using the imported prompt
code_generator_agent = LlmAgent(
    name="code_generator_agent",
    model="gemini-2.5-pro",
    # Pass the pre-formatted, static string to the agent constructor.
    instruction=CODE_GENERATOR_PROMPT,
)
