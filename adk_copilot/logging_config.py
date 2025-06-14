# FILE: adk_copilot/logging_config.py

import logging
from pathlib import Path

def _configure_logger():
    """A private function to configure and return an isolated logger instance."""

    # --- Use absolute paths for robustness ---
    project_root = Path(__file__).parent.parent
    log_dir = project_root / "logs"
    log_file_path = log_dir / "copilot.log"
    log_dir.mkdir(exist_ok=True)

    # Get a specific, named logger for our application
    log_instance = logging.getLogger("adk_copilot")
    log_instance.setLevel(logging.INFO)

    # --- KEY FIX 1: Isolate this logger from the root logger ---
    # This prevents the web server's config from affecting our file handler.
    log_instance.propagate = False
    # -----------------------------------------------------------

    # Prevent adding the file handler multiple times
    if any(isinstance(h, logging.FileHandler) for h in log_instance.handlers):
        return log_instance

    # --- KEY FIX 2: Only add the FileHandler ---
    # The web server handles console output, we only need to handle file output.
    file_handler = logging.FileHandler(log_file_path, mode='a')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    log_instance.addHandler(file_handler)
    # --- No more console handler ---

    return log_instance

# Create the logger instance that the rest of the application will import
logger = _configure_logger()