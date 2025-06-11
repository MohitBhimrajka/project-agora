import os
import sys
import argparse
import vertexai
from dotenv import load_dotenv
from google.api_core.exceptions import NotFound

# Correctly import AdkApp and use agent_engines
from adk_copilot.agent import root_agent
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

def main():
    """Deploys or deletes the ADK Copilot agent on Vertex AI Agent Engine."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="Deploy or delete the ADK Copilot agent.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", action="store_true", help="Create and deploy a new agent.")
    group.add_argument("--delete", action="store_true", help="Delete a deployed agent.")
    parser.add_argument("--resource_id", type=str, help="The full resource name of the agent to delete (required for --delete).")

    args = parser.parse_args()

    # --- Configuration and Validation ---
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    staging_bucket = f'gs://{os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")}'

    if not all([project_id, location, staging_bucket]):
        print("Error: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_STORAGE_BUCKET must be set.", file=sys.stderr)
        sys.exit(1)
        
    if args.delete and not args.resource_id:
        print("Error: --resource_id is required for --delete.", file=sys.stderr)
        sys.exit(1)

    vertexai.init(project=project_id, location=location, staging_bucket=staging_bucket)

    # --- Agent Deletion Logic ---
    if args.delete:
        try:
            print(f"Attempting to delete agent: {args.resource_id}...")
            agent_to_delete = agent_engines.get(args.resource_id)
            agent_to_delete.delete()
            print(f"✅ Successfully deleted agent: {args.resource_id}")
        except NotFound:
            print(f"Error: Agent with resource ID '{args.resource_id}' not found.", file=sys.stderr)
        except Exception as e:
            print(f"An error occurred during deletion: {e}", file=sys.stderr)
        return

    # --- Agent Creation Logic ---
    if args.create:
        # 1. Build the wheel file.
        print("Building agent wheel file using 'poetry build'...")
        build_command = "poetry build --format=wheel"
        result = os.system(build_command)
        if result != 0:
            print("Error: Poetry build failed.", file=sys.stderr)
            sys.exit(1)
        
        try:
            dist_dir = "dist"
            wheel_files = [f for f in os.listdir(dist_dir) if f.endswith(".whl")]
            agent_whl_path = os.path.join(dist_dir, wheel_files[0])
            print(f"Found wheel file: {agent_whl_path}")
        except (FileNotFoundError, IndexError):
            print(f"Build failed: No wheel file found in '{dist_dir}'.", file=sys.stderr)
            sys.exit(1)

        # 2. Define Environment Variables for the deployed agent.
        env_vars = {
            "RAG_CORPUS_NAME": os.getenv("RAG_CORPUS_NAME", ""),
            "BQ_PROJECT_ID": os.getenv("BQ_PROJECT_ID", ""),
            "BQ_DATASET_ID": os.getenv("BQ_DATASET_ID", ""),
            "GOOGLE_GENAI_USE_VERTEXAI": "1",
        }
        
        if not all([env_vars["RAG_CORPUS_NAME"], env_vars["BQ_PROJECT_ID"], env_vars["BQ_DATASET_ID"]]):
             print("Error: RAG_CORPUS_NAME, BQ_PROJECT_ID, and BQ_DATASET_ID must be set in .env before deployment.", file=sys.stderr)
             sys.exit(1)

        # 3. Wrap the agent in an AdkApp object.
        app = AdkApp(agent=root_agent, enable_tracing=True)

        # 4. Deploy using agent_engines.create() with the correct parameters.
        print("Deploying agent using agent_engines.create... This may take several minutes.")
        remote_agent = agent_engines.create(
            app,
            display_name="ADK-Copilot",
            requirements=[
                agent_whl_path,
                "google-cloud-aiplatform[adk,agent_engines]>=1.93.0",
                "sqlglot>=26.10.1",
                "db-dtypes>=1.4.2",
            ],
            extra_packages=[agent_whl_path],
            env_vars=env_vars,
        )

        print("\n✅ Agent deployed successfully!")
        print(f"Resource Name: {remote_agent.resource_name}")
        print("\nYou can now interact with your agent via the Vertex AI Console or API.")

if __name__ == "__main__":
    main()