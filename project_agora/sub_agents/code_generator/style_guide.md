# ADK Solutions Architecture: Style Guide & Best Practices

**Objective:** Generate a complete, high-quality, multi-file Python application using the Google Agent Development Kit (ADK) that is robust, secure, and ready for use.

---

### 1. Mandatory Project Structure
Every generated project MUST adhere to the following directory structure. `your_agent_name` should be a descriptive, lowercase name based on the user's request (e.g., `weather_agent`).

```
.
├── pyproject.toml
├── README.md
└── your_agent_name/
    ├── __init__.py
    ├── agent.py
    ├── config.py
    ├── prompts.py
    └── tools.py
```

---

### 2. Code Generation Best Practices

#### 2.1. ADK Import Paths (Mandatory)
You MUST use the full, explicit import paths for all ADK components. Do NOT use relative or generic top-level imports.

-   **For Agents:** `from google.adk.agents import Agent, LlmAgent`
-   **For Tools:** `from google.adk.tools import tool`
-   **For AgentTools:** `from google.adk.tools.agent_tool import AgentTool`
-   **For Tool Context:** `from google.adk.tools import ToolContext`
-   **For Callbacks:** `from google.adk.agents.callback_context import CallbackContext`

#### 2.2. Tool Error Handling (Mandatory)
All custom tools that perform I/O operations (file access, API calls) MUST include robust error handling using `try...except` blocks.

-   **Log errors** using `logging.error()`.
-   **Return user-friendly error messages** as a string. Do NOT let the tool crash.

**Example:**
```python
import logging
import requests

logger = logging.getLogger(__name__)

def call_external_api(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = "API call failed: {}".format(e)
        logger.error(error_msg)
        return "Error: Could not retrieve data. {}".format(error_msg)
```

#### 2.3. API Keys & Secrets Management (Mandatory)
-   Tools MUST NOT contain hardcoded API keys, passwords, or other secrets.
-   Secrets MUST be loaded from environment variables using `os.getenv()`.
-   The tool MUST handle cases where the environment variable is not set.

**Example:**
```python
import os
import logging

logger = logging.getLogger(__name__)

def get_weather_data(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        error_msg = "WEATHER_API_KEY environment variable not set."
        logger.error(error_msg)
        return "Error: Service is not configured. {}".format(error_msg)
    # ... logic to use the api_key ...
```

#### 2.4. Tool Logging (Mandatory)
Every custom tool function in `tools.py` MUST include logging statements to announce its execution and key parameters. This is critical for debugging.

-   Use Python's built-in `logging` module.
-   Use `.format()` to avoid conflicts with ADK's prompt templating.

**Example:**
```python
import logging
logger = logging.getLogger(__name__)

def my_tool(param: str) -> str:
    logger.info("Tool 'my_tool' called with param: {}".format(param))
    # ... tool logic ...
    return "result"
```

#### 2.5. Security: Input Sanitization
Tools that construct file paths or system commands MUST sanitize inputs to prevent security vulnerabilities.

-   Use `os.path.join()` to construct file paths safely.
-   NEVER pass raw user input directly to shell commands or SQL queries.

**Example (Safe File Path):**
```python
import os

def read_project_file(filename: str) -> str:
    # Sanitize filename to prevent path traversal (e.g., '../../etc/passwd')
    safe_filename = os.path.basename(filename)
    base_dir = "/app/data"
    safe_path = os.path.join(base_dir, safe_filename)
    # ... rest of the logic ...
```

---

### 3. Core ADK Rules

#### 3.1. File Content Requirements
-   **`pyproject.toml`:** Must include project metadata and `google-adk` as a dependency.
-   **`your_agent_name/__init__.py`:** Must contain exactly: `from .agent import root_agent`
-   **`your_agent_name/agent.py`:** Must define the `root_agent`.
-   **`your_agent_name/prompts.py`:** Must contain agent instruction prompts.
-   **`your_agent_name/tools.py`:** Must contain custom Python tools.
-   **`README.md`:** Must be generated with an overview and `adk run`/`adk web` commands.

#### 3.2. FORBIDDEN PATTERNS
-   You MUST NOT generate a `main.py` file.
-   You MUST NOT use `if __name__ == '__main__':` blocks.
-   You MUST NOT use `asyncio.run()` or `runner.run_user_message()`.

---

### 4. Final Output Formatting

#### 4.1. Mandatory "Next Steps" Section
Your final explanation MUST include a "Next Steps" section formatted exactly like this:

## Next Steps

1. Save the generated files to your local machine, maintaining the directory structure.
2. In your terminal, navigate to the project root (where pyproject.toml is) and run `poetry install` to set up the dependencies.
3. Run the agent from your terminal using the ADK CLI:
   - For a command-line interface: `adk run <your_agent_name>`
   - For the web interface: `adk web` (and select `<your_agent_name>` from the dropdown)

#### 4.2. Mermaid Syntax Rules
- **Keep it Simple:** Use simple, single-word identifiers for nodes (e.g., `UserRequest`, `Orchestrator`, `GreetTool`).
- **Use Quotes for Labels:** If a node label contains spaces or special characters, enclose the entire label in double quotes.
- **Avoid Parentheses/Brackets in Labels:** Node labels MUST NOT contain `()` or `[]`. Use simple text. Example: `MyTool["my_tool_function"]`.
- **No HTML Tags:** Node labels MUST NOT contain any HTML tags, such as `<br>` or `<br/>`. Keep labels as plain text.