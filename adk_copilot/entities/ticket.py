"""
Defines the Pydantic data models for the ADK Copilot.

These models, SupportTicket and TicketAnalysis, provide structured data handling
for managing the application's state throughout the multi-agent workflow.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    """Structured analysis of a developer request."""

    urgency: str = Field(
        default="Medium", description="Estimated urgency (e.g., Low, Medium, High)."
    )
    category: str = Field(
        default="General Inquiry",
        description="The primary category of the request (e.g., Technical, Code Generation).",
    )
    sentiment: str = Field(
        default="Neutral",
        description="The developer's sentiment (e.g., Positive, Neutral, Negative).",
    )
    summary: str = Field(
        description="A brief, one-sentence summary of the developer's issue."
    )


class SupportTicket(BaseModel):
    """The central state object representing a developer request."""

    ticket_id: str = Field(description="The unique identifier for the request.")
    customer_id: str = Field(
        description="The ID of the developer who submitted the request."
    )
    status: str = Field(
        default="New",
        description="The current status of the request in its lifecycle (e.g., New, Analyzing, Pending Solution, Resolved).",
    )
    request: str = Field(
        description="The original, verbatim request from the developer."
    )

    # Fields to be populated by the agents
    analysis: Optional[TicketAnalysis] = Field(
        default=None, description="The structured analysis of the request."
    )
    retrieved_docs: List[str] = Field(
        default_factory=list,
        description="Relevant documents or snippets from the knowledge base.",
    )
    suggested_solution: Optional[str] = Field(
        default=None,
        description="The final proposed solution to be sent to the developer.",
    )

    # History and logging
    resolution_history: List[str] = Field(
        default_factory=list, description="A log of actions taken on this request."
    )
    assigned_agent: Optional[str] = Field(
        default=None,
        description="The specialist agent currently assigned to the request.",
    )

    def to_json(self) -> str:
        """Converts the SupportTicket object to a JSON string for state management."""
        return self.model_dump_json(indent=2)
