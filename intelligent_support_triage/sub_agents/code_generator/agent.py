# FILE: intelligent_support_triage/sub_agents/code_generator/agent.py

from google.adk.agents import LlmAgent

code_generator_agent = LlmAgent(
    name="code_generator_agent",
    model="gemini-2.5-pro-preview-05-06", # Using 1.5 Pro for better reasoning
    instruction="""
        You are an Expert ADK Solutions Architect. Your role is to write complete,
        high-quality Python code for the Google Agent Development Kit based on a developer's request.

        - Analyze the user's request and the provided context.
        - Generate complete, runnable Python code snippets.
        - Format all code using markdown's python block (```python).
        - Add comments to the code to explain key parts.
        - Provide a brief explanation of the code's design and how it works.
    """,
    # REMOVE THE CALLBACK
)