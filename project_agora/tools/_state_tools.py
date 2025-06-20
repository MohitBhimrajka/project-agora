"""State management tools for Project Agora."""

import json
import uuid

from google.adk.tools import ToolContext

from ..entities.ticket import SupportTicket, TicketAnalysis
from .exceptions import StateError


def create_ticket(request: str, tool_context: ToolContext) -> str:
    """Creates a new developer request and initializes the workflow state."""
    try:
        ticket = SupportTicket(
            ticket_id=f"TICK-{str(uuid.uuid4())[:8].upper()}",
            customer_id=f"DEV-{str(uuid.uuid4())[:8].upper()}",
            request=request,
            status="New",
        )
        ticket_json = ticket.to_json()
        tool_context.state["ticket"] = ticket_json
        print("INFO: New developer request created via tool and state initialized.")
        return ticket_json
    except Exception as e:
        raise StateError(f"Failed to create ticket: {e}")


def update_ticket_after_analysis(analysis_json: str, tool_context: ToolContext) -> str:
    """Parses the analysis JSON, updates the main request object in the state."""
    try:
        # Clean JSON string first
        cleaned_json = analysis_json.strip()
        if cleaned_json.startswith("```json"):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.startswith("```"):
            cleaned_json = cleaned_json[3:]
        if cleaned_json.endswith("```"):
            cleaned_json = cleaned_json[:-3]
        cleaned_json = cleaned_json.strip()

        # Get ticket from state
        ticket_dict = json.loads(tool_context.state.get("ticket", "{}"))
        if not ticket_dict:
            raise StateError("Request not found in state.")

        # Parse analysis
        try:
            analysis_data = json.loads(cleaned_json)
        except json.JSONDecodeError:
            # Fallback parsing
            analysis_data = {
                "urgency": "Medium",
                "category": "General Inquiry", 
                "sentiment": "Neutral",
                "summary": "Analysis parsing failed - using defaults"
            }
            print(f"WARNING: Could not parse analysis JSON: {cleaned_json[:200]}")

        # Update ticket
        ticket_dict["analysis"] = TicketAnalysis(**analysis_data).model_dump()
        ticket_dict["status"] = "Analyzing"
        ticket_dict["resolution_history"].append(f"Analysis completed: {analysis_data.get('category', 'Unknown')}")

        # Save to state
        updated_ticket_json = json.dumps(ticket_dict, indent=2)
        tool_context.state["ticket"] = updated_ticket_json

        print(f"INFO: Ticket status updated to 'Analyzing'. Category: {analysis_data.get('category')}")
        return f"Ticket updated successfully. Status: Analyzing. Category: {analysis_data.get('category')}"

    except Exception as e:
        error_msg = f"Error processing analysis: {e}"
        print(f"ERROR: {error_msg}")
        raise StateError(error_msg)


def update_ticket_after_retrieval(
    kb_results: str, db_results: str, tool_context: ToolContext
) -> str:
    """Updates the ticket after knowledge retrieval and sets status to AwaitingContextConfirmation."""
    try:
        ticket_dict = json.loads(tool_context.state.get("ticket", "{}"))
        if not ticket_dict:
            raise StateError("Ticket not found in state.")

        # Store retrieval results
        ticket_dict["retrieved_kb_docs"] = kb_results
        ticket_dict["retrieved_db_tickets"] = db_results
        ticket_dict["status"] = "AwaitingContextConfirmation"
        ticket_dict["resolution_history"].append("Retrieval completed - awaiting user confirmation")

        # Save to state
        updated_ticket_json = json.dumps(ticket_dict, indent=2)
        tool_context.state["ticket"] = updated_ticket_json

        print("INFO: Ticket status updated to 'AwaitingContextConfirmation'.")
        return "Ticket updated successfully. Status: AwaitingContextConfirmation. Ready for user confirmation."

    except Exception as e:
        error_msg = f"Error updating ticket after retrieval: {e}"
        print(f"ERROR: {error_msg}")
        raise StateError(error_msg) 