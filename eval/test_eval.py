import pathlib

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_eval_full_conversation():
    """Test the agent's basic ability on a few examples."""
    await AgentEvaluator.evaluate(
        agent_module="rag",
        eval_dataset_file_path_or_dir=str(
            pathlib.Path(__file__).parent / "data/conversation.test.json"
        ),
        num_runs=1,
    )
