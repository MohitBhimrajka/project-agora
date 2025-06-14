# FILE: adk_copilot/__init__.py

# By importing the logging_config module, we ensure the logger
# is configured once when the package is first loaded.
from . import logging_config
from .agent import root_agent

logging_config.logger.info("ADK Copilot application starting up. Logging configured.")

__all__ = ["root_agent"]