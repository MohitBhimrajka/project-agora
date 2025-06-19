import asyncio
import json
import pathlib
import time

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables from .env file."""
    dotenv.load_dotenv()


def load_test_cases():
    """Load individual test cases from the JSON file."""
    test_file_path = pathlib.Path(__file__).parent / "data/conversation.test.json"
    with open(test_file_path, "r") as f:
        return json.load(f)


# Use pytest.mark.parametrize to create a separate test for each conversation
@pytest.mark.parametrize("test_case", load_test_cases())
@pytest.mark.asyncio
async def test_eval_conversation(test_case):
    """
    Test the agent on a single conversation case.
    A delay is added after each test to avoid hitting API rate limits.
    """
    # Create a temporary file for the single test case
    temp_eval_file = pathlib.Path(__file__).parent / "data/temp_eval_case.json"
    with open(temp_eval_file, "w") as f:
        json.dump([test_case], f) # AgentEvaluator expects a list

    print(f"\n--- Running test for query: '{test_case['query']}' ---")

    try:
        await AgentEvaluator.evaluate(
            agent_module="adk_copilot",
            eval_dataset_file_path_or_dir=str(temp_eval_file),
            num_runs=1,
            criteria={'response_match_score': 0.5, 'tool_trajectory_avg_score': 1.0}

        )
    finally:
        # Clean up the temporary file
        if temp_eval_file.exists():
            temp_eval_file.unlink()
        
        # This is the crucial fix: wait before starting the next test
        print(f"--- Test finished. Waiting 20 seconds to avoid rate limiting... ---")
        time.sleep(20)