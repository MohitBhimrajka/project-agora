from pydantic import BaseModel, Field
from typing import List, Optional

class TicketAnalysis(BaseModel):
    """Structured analysis of a support ticket."""
    urgency: str = Field(default="Medium", description="Estimated urgency (e.g., Low, Medium, High).")
    category: str = Field(default="General Inquiry", description="The primary category of the ticket (e.g., Technical, Billing).")
    sentiment: str = Field(default="Neutral", description="The customer's sentiment (e.g., Positive, Neutral, Negative).")
    summary: str = Field(description="A brief, one-sentence summary of the customer's issue.")

class SupportTicket(BaseModel):
    """The central state object representing a customer support ticket."""
    ticket_id: str = Field(description="The unique identifier for the ticket.")
    customer_id: str = Field(description="The ID of the customer who submitted the ticket.")
    status: str = Field(default="New", description="The current status of the ticket in its lifecycle (e.g., New, Analyzing, Pending Solution, Resolved).")
    request: str = Field(description="The original, verbatim request from the customer.")
    
    # Fields to be populated by the agents
    analysis: Optional[TicketAnalysis] = Field(default=None, description="The structured analysis of the ticket.")
    retrieved_docs: List[str] = Field(default_factory=list, description="Relevant documents or snippets from the knowledge base.")
    suggested_solution: Optional[str] = Field(default=None, description="The final proposed solution to be sent to the customer.")
    
    # History and logging
    resolution_history: List[str] = Field(default_factory=list, description="A log of actions taken on this ticket.")
    assigned_agent: Optional[str] = Field(default=None, description="The specialist agent currently assigned to the ticket.")

    def to_json(self) -> str:
        """Converts the SupportTicket object to a JSON string for state management."""
        return self.model_dump_json(indent=2)