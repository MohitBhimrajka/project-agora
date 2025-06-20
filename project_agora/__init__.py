# FILE: project_agora/__init__.py

# By importing the logging_config module, we ensure the logger
# is configured once when the package is first loaded.
from . import logging_config
from .agent import root_agent

logging_config.logger.info("Project Agora application starting up. Logging configured.")

__all__ = ["root_agent"]