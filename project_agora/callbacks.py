# FILE: project_agora/callbacks.py

import json

# Corrected imports from previous steps
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext

from .logging_config import logger # Import our configured logger

def before_agent_call(callback_context: CallbackContext):
    """Logs the start of an agent's turn."""
    logger.info("Orchestrator turn started.")
    # We can still access the state to get ticket info
    if "ticket" in callback_context.state:
        try:
            ticket = json.loads(callback_context.state["ticket"])
            logger.info("Current Ticket ID: %s, Status: %s", ticket.get('ticket_id'), ticket.get('status'))
        except (json.JSONDecodeError, TypeError):
            logger.warning("Could not parse ticket from state during before_agent_call.")


def before_tool_call(tool: object, args: dict, tool_context: ToolContext):
    """Logs information before a tool is called."""
    if tool.name in ["load_artifacts", "code_interpreter"]:
        return
    logger.info("Orchestrator calling tool '%s' with args: %s", tool.name, args)


def after_tool_call(tool: object, args: dict, tool_context: ToolContext, tool_response: str):
    """Logs information after a tool has been called."""
    if tool.name in ["load_artifacts", "code_interpreter"]:
        return
    # Truncate long tool responses for cleaner logs
    if isinstance(tool_response, str):
        truncated_response = (
            tool_response[:250] + "..." if len(tool_response) > 250 else tool_response
        )
    else:
        truncated_response = str(tool_response)

    logger.info(
        "Tool '%s' finished. Response: %s", tool.name, truncated_response
    )