"""Custom exceptions for ADK Copilot tools."""


class ToolError(Exception):
    """Base class for tool-related errors."""
    pass


class ConfigurationError(ToolError):
    """Raised when a required configuration is missing."""
    pass


class GCSInteractionError(ToolError):
    """Raised for errors interacting with Google Cloud Storage."""
    pass


class BigQueryError(ToolError):
    """Raised for errors during BigQuery operations."""
    pass


class StateError(ToolError):
    """Raised for errors related to state management."""
    pass


class EmbeddingError(ToolError):
    """Raised for errors during embedding generation."""
    pass


class DiagramGenerationError(ToolError):
    """Raised for errors during diagram generation."""
    pass 