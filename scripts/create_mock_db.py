# FILE: scripts/create_mock_db.py

import csv
import os

def generate_mock_data():
    """
    Generates a comprehensive CSV file with mock ADK-specific support ticket data,
    based on a real-world debugging and development session.
    """
    data = [
        ["ticket_id", "customer_id", "request", "category", "suggested_solution"],
        
        # --- Orchestration & Core Concepts ---
        ["ADK-101", "DEV-101", "How do I make my agents call each other in a specific, multi-step sequence? My main agent just stops after the first step.", "Orchestration", "The best practice is to use a strong, sequential prompt for the main orchestrator agent. List the tools/sub-agents to be called in order (e.g., Step A, Step B, Step C) and instruct the orchestrator to use the output of one step as the input for the next. Do not rely on complex callback logic for orchestration."],
        ["ADK-102", "DEV-102", "What is the best way to handle different types of user queries, like greetings vs actual support tickets?", "Intent Analysis", "Implement a 'gatekeeper' or 'intent analysis' pattern in your main orchestrator's prompt. Instruct the agent to first classify the user's intent. If it's a simple conversation (greeting, thank you, etc.), it should answer directly without calling any tools. If it's a genuine support issue, it should then trigger the full tool-calling workflow."],
        ["ADK-103", "DEV-103", "How should I pass data between different sub-agents in my workflow?", "State Management", "While `tool_context.state` can be used, a more robust pattern for sequential workflows is to have the orchestrator manage the flow. The orchestrator should receive the full output from one tool call (e.g., a JSON string from an analysis agent), parse it in its own reasoning process, and then pass the relevant, cleaned-up pieces of data as arguments to the next tool in the sequence."],

        # --- Framework Errors & Gotchas ---
        ["ADK-201", "DEV-201", "My app crashes on start with a Pydantic `ValidationError` for an 'extra_forbidden' parameter like 'response_model' or 'state_model'.", "Agent Definition", "This error means you are passing a parameter that the `google.adk.agents.Agent` class does not recognize. The base `Agent` class does not accept `response_model` or `state_model`. To get structured output, prompt the agent to return raw JSON. To initialize state, use a dedicated 'intake' tool as the first step of your workflow rather than a callback."],
        ["ADK-202", "DEV-202", "My `before_agent_callback` is throwing an `AttributeError: 'CallbackContext' object has no attribute 'conversation_history'`.", "Callbacks", "This happens because the `before_agent_callback` receives a lightweight `CallbackContext`, which only contains the `state`, not the full `conversation_history`. If you need to access the user's initial query to create a state object, it is more reliable to create a dedicated 'intake' tool (e.g., `create_ticket`) that the agent calls as its very first action."],
        ["ADK-203", "DEV-203", "My callback function `my_func(ctx)` is failing with a `TypeError` about an unexpected keyword argument `callback_context`.", "Callbacks", "This `TypeError` means the parameter name in your function definition does not match what the ADK framework provides. You must rename your function's parameter to match the framework's keyword. For `before_agent_callback`, the correct signature is `def my_func(callback_context: InvocationContext):`."],

        # --- Tool & API Errors ---
        ["ADK-301", "DEV-301", "I'm getting a `400 INVALID_ARGUMENT` error saying 'Multiple tools are supported only when they are all search tools'.", "Tool Integration", "The Google API has a constraint that does not allow mixing the built-in `VertexAiRagRetrieval` tool with other custom Python function tools within the same agent's tool list. The correct pattern is to isolate the `VertexAiRagRetrieval` tool in its own dedicated agent, and then create a separate agent for your other custom tools. The orchestrator can then call these agents sequentially."],
        ["ADK-302", "DEV-302", "My RAG tool is failing with a Python error: `TypeError: 'RagContexts' object is not iterable`.", "RAG / Tool Implementation", "This error occurs when you incorrectly try to iterate over the main response object from the `vertexai.rag.retrieval_query` function. The correct way to access the retrieved documents is to iterate over the `.contexts` attribute of the response object, like so: `for ctx in response.contexts:`."],
        ["ADK-303", "DEV-303", "My BigQuery tool is failing with a `400 Unrecognized name: request` error from the database.", "Tool Implementation / SQL", "This is a standard SQL error caused by column name ambiguity, especially in a `WHERE` clause. The most robust fix is to assign an alias to your table in the `FROM` clause (e.g., `FROM my_dataset.my_table AS t`) and then qualify all column references with that alias (e.g., `WHERE t.column_name = ...`)."],
        
        # --- Environment & Configuration ---
        ["ADK-401", "DEV-401", "My app is crashing with `ModuleNotFoundError: No module named 'llama_index'` when I try to use the RAG tool.", "Dependencies / Setup", "The ADK's built-in `VertexAiRagRetrieval` tool requires `llama-index` as a peer dependency. To fix this, you must explicitly add `llama-index = \"^0.12.1\"` (or a compatible version) to your `pyproject.toml` file and then run `poetry install` to update your environment."],
        ["ADK-402", "DEV-402", "My agent is failing with a `404 NOT_FOUND` error for a model like `gemini-2.5-pro-preview-05-06`.", "Configuration", "A `404 NOT_FOUND` error for a model means the model name is either incorrect or not available in your specified GCP project and region. Check the official Google Cloud documentation for valid, available model names (e.g., 'gemini-2.5-pro-preview-05-06', 'gemini-2.0-flash-001') and update your agent definitions accordingly."]
    ]

    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filepath = os.path.join(output_dir, "resolved_tickets.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"✅ Extensive mock ADK specialist database created at '{filepath}' with {len(data)-1} tickets.")

if __name__ == "__main__":
    generate_mock_data()