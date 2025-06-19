# FILE: adk_copilot/tools/tools.py

import json
import os
import tempfile
import uuid

from google.adk.tools import ToolContext
from google.cloud import bigquery
from google.cloud import storage
from playwright.async_api import async_playwright
from vertexai.language_models import TextEmbeddingModel

from ..entities.ticket import SupportTicket, TicketAnalysis


def _get_embedding_for_query(
    text: str, model_name: str = "text-embedding-004"
) -> list[float]:
    """Helper function to generate an embedding for the user's query."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    try:
        embeddings = model.get_embeddings([text])
        return embeddings[0].values
    except Exception as e:
        print(f"ERROR: Could not get embedding for query: {e}")
        return None


def create_ticket(request: str, tool_context: ToolContext) -> str:
    """Creates a new developer request and initializes the workflow state."""
    ticket = SupportTicket(
        ticket_id=f"TICK-{str(uuid.uuid4())[:8].upper()}",
        customer_id=f"DEV-{str(uuid.uuid4())[:8].upper()}",
        request=request,
        status="New",
    )
    ticket_json = ticket.to_json()
    tool_context.state["ticket"] = ticket_json
    print("INFO: New developer request created via tool and state initialized.")
    return ticket_json


def search_resolved_tickets_db(query: str) -> str:
    """Performs a semantic vector search on the BigQuery database of resolved tickets."""
    print(f"INFO: Starting semantic search for query: '{query}'")

    bq_project_id = os.getenv("BQ_PROJECT_ID")
    bq_dataset_id = os.getenv("BQ_DATASET_ID")

    if not bq_project_id or not bq_dataset_id:
        return "Error: BigQuery project ID or dataset ID is not configured."

    query_embedding = _get_embedding_for_query(query)
    if not query_embedding:
        return "Error: Could not generate an embedding for the search query."

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
        return f"Error: Failed to execute database vector search. Details: {e}"


def update_ticket_after_analysis(analysis_json: str, tool_context: ToolContext) -> str:
    """Parses the analysis JSON, updates the main request object in the state."""
    try:
        # Clean JSON string first
        cleaned_json = analysis_json.strip()
        if cleaned_json.startswith("```json"):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.startswith("```"):
            cleaned_json = cleaned_json[3:]
        if cleaned_json.endswith("```"):
            cleaned_json = cleaned_json[:-3]
        cleaned_json = cleaned_json.strip()

        # Get ticket from state
        ticket_dict = json.loads(tool_context.state.get("ticket", "{}"))
        if not ticket_dict:
            return "Error: Request not found in state."

        # Parse analysis
        try:
            analysis_data = json.loads(cleaned_json)
        except json.JSONDecodeError:
            # Fallback parsing
            analysis_data = {
                "urgency": "Medium",
                "category": "General Inquiry", 
                "sentiment": "Neutral",
                "summary": "Analysis parsing failed - using defaults"
            }
            print(f"WARNING: Could not parse analysis JSON: {cleaned_json[:200]}")

        # Update ticket
        ticket_dict["analysis"] = TicketAnalysis(**analysis_data).model_dump()
        ticket_dict["status"] = "Analyzing"
        ticket_dict["resolution_history"].append(f"Analysis completed: {analysis_data.get('category', 'Unknown')}")

        # Save to state
        updated_ticket_json = json.dumps(ticket_dict, indent=2)
        tool_context.state["ticket"] = updated_ticket_json

        print(f"INFO: Ticket status updated to 'Analyzing'. Category: {analysis_data.get('category')}")
        return f"Ticket updated successfully. Status: Analyzing. Category: {analysis_data.get('category')}"

    except Exception as e:
        error_msg = f"Error processing analysis: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg


def update_ticket_after_retrieval(
    kb_results: str, db_results: str, tool_context: ToolContext
) -> str:
    """Updates the ticket after knowledge retrieval and sets status to AwaitingContextConfirmation."""
    try:
        ticket_dict = json.loads(tool_context.state.get("ticket", "{}"))
        if not ticket_dict:
            return "Error: Ticket not found in state."

        # Store retrieval results
        ticket_dict["retrieved_kb_docs"] = kb_results
        ticket_dict["retrieved_db_tickets"] = db_results
        ticket_dict["status"] = "AwaitingContextConfirmation"
        ticket_dict["resolution_history"].append("Retrieval completed - awaiting user confirmation")

        # Save to state
        updated_ticket_json = json.dumps(ticket_dict, indent=2)
        tool_context.state["ticket"] = updated_ticket_json

        print("INFO: Ticket status updated to 'AwaitingContextConfirmation'.")
        return "Ticket updated successfully. Status: AwaitingContextConfirmation. Ready for user confirmation."

    except Exception as e:
        error_msg = f"Error updating ticket after retrieval: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg


async def generate_diagram_from_mermaid(mermaid_code: str, file_name: str) -> str:
    """
    Renders Mermaid diagram syntax into a PNG image, uploads it to Google Cloud
    Storage, and returns its public URL. This is an async function.

    Args:
        mermaid_code: The Mermaid syntax string to be rendered.
        file_name: The desired base name for the output file (e.g., 'architecture_plan').

    Returns:
        The public URL of the generated diagram image in GCS, or an error string.
    """
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    if not bucket_name:
        return "Error: GOOGLE_CLOUD_STORAGE_BUCKET environment variable not set."

    # --- FIX 1: Un-escape the mermaid code ---
    # Convert escaped newlines and quotes from the JSON string back to their literal versions
    processed_mermaid_code = mermaid_code.replace('\\n', '\n').replace('\\"', '"')
    # --- END OF FIX 1 ---

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>mermaid.initialize({{ startOnLoad: true }});</script>
    </head>
    <body>
        <div class="mermaid">{processed_mermaid_code}</div>
    </body>
    </html>
    """

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html_template)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                diagram_element = page.locator(".mermaid")
                await diagram_element.screenshot(path=tmp_file.name)
                tmp_file_path = tmp_file.name

            await browser.close()
        except Exception as e:
            return f"Error during Playwright rendering: {e}"

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # --- FIX 2: Correct the filename logic ---
        # Get the base name of the file, stripping any extension
        base_name, _ = os.path.splitext(file_name)
        # Construct the destination path with a single, correct .png extension
        destination_blob_name = f"diagrams/{base_name}.png"
        # --- END OF FIX 2 ---
        
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(tmp_file_path)
        os.remove(tmp_file_path)

        print(f"INFO: Diagram uploaded to gs://{bucket_name}/{destination_blob_name}")
        # Make the blob public to get a URL.
        # Note: In production, you would use signed URLs for security.
        blob.make_public()
        return blob.public_url
    except Exception as e:
        return f"Error: Failed to upload diagram to GCS. Details: {e}"
    
    
def format_code_reviewer_output(reviewer_json_output: str) -> str:
    """
    Simpler, more robust version that handles the JSON parsing better.
    """
    try:
        # Clean the JSON string
        cleaned = reviewer_json_output.strip()
        
        # Remove markdown blocks if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        # Try to parse JSON
        try:
            data = json.loads(cleaned)
            status = data.get("status", "").lower()
            
            if status == "approved":
                # Get the code and clean it up
                code = data.get("code", "")
                # Simple unescape - just handle the most common cases
                clean_code = code.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                
                return f"""✅ **Code Review: APPROVED**

The code has been generated and has passed all quality checks. Here is the complete, multi-file agent:

{clean_code}"""
            
            elif status == "rejected":
                feedback = data.get("feedback", "Code review failed")
                corrected_code = data.get("corrected_code", "")
                clean_corrected = corrected_code.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                
                return f"""⚠️ **Code Review: ISSUES CORRECTED**

**Issues Found and Fixed:**
{feedback}

**Corrected Code:**
{clean_corrected}"""
                
        except json.JSONDecodeError:
            # If JSON parsing fails completely, try to extract the code manually
            # Look for the actual code content in the string
            if '"status": "approved"' in cleaned:
                # Find the code section - look for the FILE markers
                start_marker = '==== FILE:'
                if start_marker in cleaned:
                    # Extract everything from the first FILE marker onwards
                    start_pos = cleaned.find(start_marker)
                    if start_pos != -1:
                        # Find the end of the code section
                        raw_code = cleaned[start_pos:]
                        # Clean up the most obvious escaping
                        clean_code = raw_code.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                        
                        return f"""✅ **Code Review: APPROVED**

The code has been generated and has passed all quality checks. Here is the complete, multi-file agent:

{clean_code}"""
            
            # If we can't extract anything useful, show error
            return f"""🚨 **Code Review Response Error**

Could not parse the code reviewer's response properly. The code was generated but there was a formatting issue.

Raw response (first 500 chars):
{reviewer_json_output[:500]}...

Please try generating the code again."""
            
    except Exception as e:
        return f"""🚨 **Unexpected Error**

An error occurred while processing the code review: {e}

Please try generating the code again."""


def _unescape_json_string(json_string: str) -> str:
    """
    Properly unescape a JSON string, handling newlines, quotes, and other escapes.
    """
    if not json_string:
        return ""
    
    # Unescape common JSON escape sequences
    unescaped = json_string.replace('\\n', '\n')
    unescaped = unescaped.replace('\\"', '"')
    unescaped = unescaped.replace('\\/', '/')
    unescaped = unescaped.replace('\\\\', '\\')
    unescaped = unescaped.replace('\\t', '\t')
    unescaped = unescaped.replace('\\r', '\r')
    
    return unescaped


def _extract_info_manually(text: str) -> str:
    """
    Fallback method to extract information when JSON parsing fails.
    Looks for key patterns in the text.
    """
    text_lower = text.lower()
    
    # Check for approval
    if '"status": "approved"' in text_lower or '"status":"approved"' in text_lower:
        return """⚠️ **Code Review Parsing Issue**

The code reviewer approved the code, but there was an issue formatting the output.
Please try generating the code again."""
    
    # Check for rejection
    elif '"status": "rejected"' in text_lower or '"status":"rejected"' in text_lower:
        return """⚠️ **Code Review Issues Found**

The code reviewer found issues with the generated code, but there was a formatting problem.
Please try generating the code again."""
    
    return f"""🚨 **Code Review Response Error**

Could not parse the code reviewer's response. Raw output:

{text[:1000]}...

Please try generating the code again."""