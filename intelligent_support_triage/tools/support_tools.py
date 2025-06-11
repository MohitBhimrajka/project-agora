import os
from google.adk.tools import ToolContext
from google.cloud import bigquery
from vertexai import rag

# We will define a placeholder for the BigQuery client for now.
# In a real app, you would initialize this once.
def get_bq_client():
    project_id = os.getenv("BQ_PROJECT_ID")
    return bigquery.Client(project=project_id)

def search_knowledge_base(query: str, tool_context: ToolContext) -> str:
    """
    Searches the company's knowledge base (FAQs, documentation) for articles
    relevant to the user's query.
    """
    print(f"Searching knowledge base for: {query}")
    corpus_name = os.getenv("RAG_CORPUS_NAME")
    if not corpus_name:
        return "Error: RAG_CORPUS_NAME environment variable is not set. Cannot search knowledge base."

    try:
        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
            text=query,
        )
        return str(response)
    except Exception as e:
        return f"An error occurred during RAG retrieval: {str(e)}"

def search_resolved_tickets_db(natural_language_query: str, tool_context: ToolContext) -> str:
    """
    Searches the historical database of resolved support tickets for similar issues.
    Use a natural language query to describe the problem.
    """
    print(f"Searching resolved tickets DB with query: {natural_language_query}")
    # This is a simplified version of the data-science NL2SQL tool.
    # For a demo, a direct keyword-based query is often sufficient and more reliable.
    # In a production system, you would use the more advanced Chase-SQL implementation.
    
    project_id = os.getenv("BQ_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID")
    
    # Simple query generation for the demo
    # WARNING: This is a simplified implementation for demonstration purposes.
    # It is vulnerable to SQL injection if not handled carefully.
    # A production system should use parameterized queries or a safer query-building library.
    sql_query = f"""
    SELECT
        request,
        suggested_solution
    FROM
        `{project_id}.{dataset_id}.resolved_tickets`
    WHERE
        request LIKE '%{natural_language_query.replace("'", "''")}%'
    LIMIT 3
    """

    try:
        client = get_bq_client()
        query_job = client.query(sql_query)
        results = query_job.result()
        
        if results.total_rows == 0:
            return "No similar resolved tickets found in the database."

        # Format results for the agent
        formatted_results = []
        for row in results:
            formatted_results.append(f"Similar Request: {row.request}\nProvided Solution: {row.suggested_solution}\n---")
            
        return "\n".join(formatted_results)

    except Exception as e:
        return f"An error occurred while querying BigQuery: {str(e)}"