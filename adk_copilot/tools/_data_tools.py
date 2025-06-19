"""Data retrieval tools for ADK Copilot."""

import os

from google.cloud import bigquery
from vertexai.language_models import TextEmbeddingModel

from .exceptions import ConfigurationError, BigQueryError, EmbeddingError


def _get_embedding_for_query(
    text: str, model_name: str = "text-embedding-004"
) -> list[float]:
    """Helper function to generate an embedding for the user's query."""
    try:
        model = TextEmbeddingModel.from_pretrained(model_name)
        embeddings = model.get_embeddings([text])
        return embeddings[0].values
    except Exception as e:
        print(f"ERROR: Could not get embedding for query: {e}")
        raise EmbeddingError(f"Could not get embedding for query: {e}")


def search_resolved_tickets_db(query: str) -> str:
    """Performs a semantic vector search on the BigQuery database of resolved tickets."""
    print(f"INFO: Starting semantic search for query: '{query}'")

    bq_project_id = os.getenv("BQ_PROJECT_ID")
    bq_dataset_id = os.getenv("BQ_DATASET_ID")

    if not bq_project_id or not bq_dataset_id:
        raise ConfigurationError("BigQuery project ID or dataset ID is not configured.")

    try:
        query_embedding = _get_embedding_for_query(query)
    except EmbeddingError:
        raise

    client = bigquery.Client(project=bq_project_id)
    table_id = f"{bq_project_id}.{bq_dataset_id}.resolved_tickets"

    sql_query = f"""
        SELECT
            ticket_id,
            request,
            category,
            suggested_solution,
            -- Calculate the cosine distance between the query vector and the stored embeddings
            COSINE_DISTANCE(request_embedding, @query_embedding) as distance
        FROM
            `{table_id}`
        -- Order by distance (smaller is better) and return the top 3 matches
        ORDER BY
            distance
        LIMIT 3
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("query_embedding", "FLOAT64", query_embedding),
        ]
    )

    try:
        print(f"INFO: Executing BigQuery vector search...")
        query_job = client.query(sql_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]

        if not results:
            return "[]"

        return str(results)

    except Exception as e:
        print(f"ERROR: BigQuery vector search failed: {e}")
        raise BigQueryError(f"Failed to execute database vector search. Details: {e}") 