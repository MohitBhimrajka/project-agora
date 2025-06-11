from google.adk.agents import LlmAgent
from ..solution_generation.agent import build_solution_context # We can reuse the same context builder

code_generator_agent = LlmAgent(
    name="code_generator_agent",
    model="gemini-2.5-pro-05-06", # Use the Pro model for high-quality code generation
    instruction="""
        You are an Expert ADK Solutions Architect. Your role is to write complete,
        high-quality Python code for the Google Agent Development Kit based on a developer's request.

        - Analyze the user's request and the provided context.
        - Generate complete, runnable Python code snippets.
        - Format all code using markdown's python block (```python).
        - Add comments to the code to explain key parts.
        - Provide a brief explanation of the code's design and how it works.
    """,
    before_agent_callback=build_solution_context,
)