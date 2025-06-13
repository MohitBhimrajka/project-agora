# ADK Solutions Architecture: Style Guide & Constraints

**Objective:** Generate a complete, high-quality, multi-file Python application using the Google Agent Development Kit (ADK) that can be run directly by the ADK CLI.

### Mandatory Project Structure
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

### File Content Requirements

1.  **`pyproject.toml`:**
    *   Must include project metadata and `google-adk` as a dependency.

2.  **`your_agent_name/__init__.py`:**
    *   Must make the package runnable by the ADK CLI.
    *   The entire content of this file MUST be: `from .agent import root_agent`

3.  **`your_agent_name/agent.py`:**
    *   This is the main file. It MUST define the primary agent instance and assign it to a variable named exactly `root_agent`.

4.  **`your_agent_name/prompts.py`:**
    *   Must contain the instruction prompts for the agent(s).

5.  **`your_agent_name/tools.py`:**
    *   Must contain the definitions for any custom Python tools.

### Code Quality & Documentation Requirements

6.  **Tool Logging (Mandatory):**
    *   Every custom tool function in `tools.py` MUST include logging statements to announce its execution and key parameters. This is critical for debugging.
    *   Use Python's built-in `logging` module.
    *   **Example:**
        ```python
        import logging
        logger = logging.getLogger(__name__)

        def my_tool(param: str) -> str:
            logger.info(f"Tool 'my_tool' called with param: {{param}}")
            # ... tool logic ...
            return "result"
        ```

7.  **Descriptive Agent Prompts (Mandatory):**
    *   The instruction prompt in `prompts.py` must not be generic. It must clearly state the agent's persona, its primary goal, and explicitly mention each tool it can use and under what circumstances.
    *   **Good Example:** `"You are a helpful weather assistant. When a user asks for the weather in a specific city, you MUST use the 'get_weather' tool to find the information."`
    *   **Bad Example:** `"You are an agent. Use your tools."`

8.  **Helpful Code Comments (Mandatory):**
    *   Add comments to `agent.py` to explain the key parts of the agent's definition, such as why a particular model was chosen or the purpose of the `tools` list.

9.  **`README.md` (Mandatory):**
    *   You MUST generate a helpful `README.md` file.
    *   It must include the following sections:
        *   A brief overview of the agent's purpose.
        *   Instructions on how to run `poetry install`.
        *   The exact `adk run` and `adk web` commands to execute the agent.

10. **`config.py` (Recommended for agents with configurable settings):**
    *   For settings like `model` names, define them in `config.py`.
    *   Use a Pydantic `BaseModel` or a simple Python class for structure.
    *   **Example `config.py`:**
        ```python
        class AgentConfig:
            MODEL_NAME = "gemini-1.5-pro-preview-0521"
        ```
    *   **Example `agent.py` usage:**
        ```python
        from .config import AgentConfig
        
        root_agent = Agent(model=AgentConfig.MODEL_NAME, ...)
        ```

### FORBIDDEN PATTERNS

-   **You MUST NOT generate a `main.py` file.**
-   **You MUST NOT use `if __name__ == '__main__':` blocks.**
-   **You MUST NOT use `asyncio.run()` or `runner.run_user_message()`.** The ADK CLI handles all execution.

### Mandatory "Next Steps" Section
Your final explanation MUST include a "Next Steps" section that instructs the user on how to run their new agent using ONLY the ADK CLI tools. The section must look like this example:

```
### Next Steps

1.  Save the generated files to your local machine, maintaining the directory structure.
2.  In your terminal, navigate to the project root (where `pyproject.toml` is) and run `poetry install` to set up the dependencies.
3.  Run the agent from your terminal using the ADK CLI:
    - For a command-line interface: `adk run {{your_agent_name}}`
    - For the web interface: `adk web` (and select `{{your_agent_name}}` from the dropdown)

### Mermaid Syntax Rules
- Node text containing special characters (like `[]()""{}`) **MUST** be enclosed in double quotes.
- Link text containing special characters **MUST** use HTML character codes to escape them.
  - For `"` use `#quot;`
  - For `{` use `#123;`
  - For `}` use `#125;`
- **Correct Example:** `A -- "Calls tool with arg: #quot;foo#quot;" --> B`
- **Incorrect Example:** `A -- "Calls tool with arg: "foo"" --> B`