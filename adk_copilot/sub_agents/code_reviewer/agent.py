# FILE: adk_copilot/sub_agents/code_reviewer/agent.py

from google.adk.agents import LlmAgent
from .prompts import CODE_REVIEWER_PROMPT

code_reviewer_agent = LlmAgent(
    name="code_reviewer_agent",
    model="gemini-2.5-pro",
    # Pass the pre-formatted string directly.
    instruction=CODE_REVIEWER_PROMPT,
)