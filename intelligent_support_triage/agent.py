from google.adk.agents import Agent
from .prompts import ORCHESTRATOR_PROMPT

# NOTE: These sub-agents do not exist yet. We will create them in Phase 2.
# We are defining them here to structure our Orchestrator correctly from the start.
from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.0-flash-001",  # A fast and capable model for routing
    instruction=ORCHESTRATOR_PROMPT,
    sub_agents=[
        ticket_analysis_agent,
        knowledge_retrieval_agent,
        solution_generation_agent,
    ],
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent