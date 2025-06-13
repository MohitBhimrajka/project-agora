# FILE: adk_copilot/sub_agents/code_reviewer/agent.py

import os
from google.adk.agents import LlmAgent

# Helper function to load the style guide from the local file
def _load_style_guide():
    """Loads the ADK style guide from a local markdown file."""
    # Construct a path relative to the current file's location
    # Note: We point back to the code_generator's style guide to avoid duplication
    style_guide_path = os.path.join(os.path.dirname(__file__), "../code_generator/style_guide.md")
    try:
        with open(style_guide_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("ERROR: adk_copilot/sub_agents/code_generator/style_guide.md not found.")
        return "Error: Style guide not found."

# Load the style guide once when the module is imported
ADK_STYLE_GUIDE = _load_style_guide()

# Construct the final prompt string at the module level, NOT inside the agent definition.
# This ensures the f-string is evaluated only once when the application starts.
REVIEWER_INSTRUCTION = f"""
You are an elite ADK Code Reviewer. Your sole purpose is to analyze a set of generated Python files for an ADK agent and ensure they are 100% correct and follow best practices.

**CRITICAL INSTRUCTIONS:**
1.  You will be given the generated code and the ADK Style Guide.
2.  You MUST meticulously check the code against the checklist below.
3.  Your output MUST be a single, raw JSON object and nothing else.

---
**ADK Style Guide to Enforce:**
{ADK_STYLE_GUIDE}
---

**Code Review Checklist:**
1.  **Imports:** Are all `google.adk` imports correct (e.g., `from google.adk.agents import Agent`)?
2.  **`root_agent` Definition:** Is there a variable named exactly `root_agent` in `agent.py`?
3.  **`__init__.py` Correctness:** Does the `__init__.py` file correctly expose the `root_agent` with `from .agent import root_agent`?
4.  **Forbidden Patterns:** Does the code contain any forbidden patterns like `main.py` or `if __name__ == '__main__':`?
5.  **Dependencies:** Does the `pyproject.toml` correctly list all necessary dependencies inferred from the code (e.g., `requests`, `playwright`)?

**Output Schema:**
- **If NO issues are found:** Return a JSON object with `status: "approved"`.
  `{{ "status": "approved", "code": "<The original, unmodified code>" }}`
- **If ANY issue is found:** You MUST correct the code. Return a JSON object with `status: "rejected"`.
  `{{ "status": "rejected", "feedback": "<A detailed, bulleted list of all errors found and corrections made>", "corrected_code": "<The complete, corrected, multi-file code string>" }}`
"""

code_reviewer_agent = LlmAgent(
    name="code_reviewer_agent",
    model="gemini-2.5-pro-preview-05-06",
    # Pass the pre-formatted string directly.
    instruction=REVIEWER_INSTRUCTION,
)