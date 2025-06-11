import json
from google.adk.agents import Agent
# CORRECTED: The callback function is passed an InvocationContext object
from google.adk.agents.invocation_context import InvocationContext
from .prompts import ORCHESTRATOR_PROMPT
from .entities.ticket import SupportTicket

from .sub_agents.ticket_analysis.agent import ticket_analysis_agent
from .sub_agents.knowledge_retrieval.agent import knowledge_retrieval_agent
from .sub_agents.solution_generation.agent import solution_generation_agent

def orchestrator_callback(ctx: InvocationContext):
    """
    This callback function implements the core workflow logic.
    It inspects the state of the ticket and routes to the correct sub-agent.
    """
    state = ctx.state

    # On first run, create the ticket object in the state
    if "ticket" not in state:
        # CORRECTED: Access the conversation history from the InvocationContext
        user_query = ctx.conversation_history[-1].content.parts[0].text

        ticket = SupportTicket(
            ticket_id="TICK-DEMO-001",
            customer_id="CUST-DEMO-123",
            request=user_query
        )
        state["ticket"] = ticket.to_json()
        state["next_agent"] = "ticket_analysis_agent"
        return

    # Load the current ticket state
    ticket_data = json.loads(state["ticket"])
    ticket = SupportTicket.model_validate(ticket_data)
    
    # CORRECTED: Get the last response from the conversation history,
    # which will be the output of the previously called sub-agent.
    last_response = ctx.conversation_history[-1].content.parts[0].text

    # == Workflow Logic ==
    # If the last step was analysis, now we retrieve knowledge
    if ticket.status == "New":
        # The last response is a JSON string from the ticket_analysis_agent
        analysis_data = json.loads(last_response)
        ticket.analysis = analysis_data
        ticket.status = "Analyzing"
        state["next_agent"] = "knowledge_retrieval_agent"
    # If the last step was retrieval, now we generate a solution
    elif ticket.status == "Analyzing":
        ticket.retrieved_docs = [last_response]
        ticket.status = "Pending Solution"
        state["next_agent"] = "solution_generation_agent"
    elif ticket.status == "Pending Solution":
        ticket.suggested_solution = last_response
        ticket.status = "Resolved"
        state["next_agent"] = None # Stop the chain

    # Save the updated ticket back to the state
    state["ticket"] = ticket.to_json()


# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.0-flash-001",
    instruction=ORCHESTRATOR_PROMPT,
    sub_agents=[
        ticket_analysis_agent,
        knowledge_retrieval_agent,
        solution_generation_agent,
    ],
    # This callback is the brain of our workflow
    before_agent_callback=orchestrator_callback,
)

# This is the root agent that the ADK will run.
root_agent = orchestrator_agent