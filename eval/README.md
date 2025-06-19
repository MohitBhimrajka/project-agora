# Evaluation Directory

This directory contains the testing and evaluation suite for the ADK Copilot. A robust evaluation process is critical for ensuring the agent behaves as expected, preventing regressions, and measuring the quality of its responses.

### Purpose of Evaluation

We evaluate the agent to verify two key aspects:
1. **Tool Use Trajectory:** Does the agent call the correct sequence of tools for a given query?
2. **Response Quality:** Is the agent's final text response accurate and relevant to the query?

### How to Run the Evaluation

To run the full evaluation suite, use `pytest` from the project's root directory. Ensure you have installed the development dependencies.

```bash
poetry run pytest eval/
```

### Understanding the Evaluation Data

The test cases are defined in `data/conversation.test.json`. Each test case is a JSON object with the following fields:

- **`query`**: (String) The input message from the user that starts the test.
- **`expected_tool_use`**: (Array of Objects) A list of the tools the agent is expected to call, in order. This is used to calculate the `tool_trajectory_avg_score`.
  - **`tool_name`**: The name of the tool or sub-agent that should be called.
- **`reference`**: (String) An ideal, "golden" answer to the user's query. This is used to calculate the `response_match_score` by measuring the semantic similarity between the agent's actual response and this reference text.

### Adding New Tests

To add a new test case:

1. Open `data/conversation.test.json`.
2. Add a new JSON object to the main array.
3. Define the `query`, `expected_tool_use`, and `reference` fields for your new scenario.
4. Run the evaluation script to see how the agent performs.

### Test Coverage

The evaluation suite covers:
- Knowledge retrieval scenarios
- Code generation workflows  
- Problem-solving requests
- Multi-step workflows requiring user confirmation
- Edge cases and error handling

This ensures comprehensive testing of the agent's capabilities across all major use cases. 