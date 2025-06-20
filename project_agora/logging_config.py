# FILE: project_agora/logging_config.py

import logging
import os
import sys
from pathlib import Path

def _configure_logger():
    """
    Configures a logger that works both locally and on Google Cloud Run.

    - When running locally, it logs to both the console and a file (`logs/agora.log`).
    - When deployed on Cloud Run, it detects the environment and logs only to the
      console stream, which is automatically captured by Cloud Logging.
    """
    # --- Detect the Environment ---
    IS_ON_CLOUD_RUN = 'K_SERVICE' in os.environ

    # Get a specific, named logger for our application
    log_instance = logging.getLogger("project_agora")
    log_instance.setLevel(logging.INFO)

    # Isolate this logger from the root logger to avoid conflicts
    log_instance.propagate = False

    # Prevent adding handlers multiple times if this function is re-imported
    if log_instance.hasHandlers():
        return log_instance

    # --- Configure Console (Stream) Handler ---
    # This is used in BOTH local and cloud environments.
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        # Use a more detailed format for clarity
        "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    log_instance.addHandler(console_handler)

    if IS_ON_CLOUD_RUN:
        # We are in the cloud. Cloud Logging handles persistence.
        log_instance.info("Cloud Run environment detected. Logging to standard output only.")
    else:
        # We are running locally. Add the FileHandler for local development.
        try:
            # Calculate absolute path for the logs directory
            project_root = Path(__file__).parent.parent
            log_dir = project_root / "logs"
            log_file_path = log_dir / "agora.log"
            log_dir.mkdir(exist_ok=True)

            # --- Configure File Handler ---
            file_handler = logging.FileHandler(log_file_path, mode='a')
            file_handler.setFormatter(formatter)
            log_instance.addHandler(file_handler)
            log_instance.info(f"Local environment detected. Logging to console and '{log_file_path}'.")
        except Exception as e:
            log_instance.error(f"Failed to configure file logging: {e}")

    return log_instance

# Create the logger instance that the rest of the application will import
logger = _configure_logger()