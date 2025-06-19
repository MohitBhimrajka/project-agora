"""Rendering and formatting tools for ADK Copilot."""

import json
import os
import tempfile

from google.cloud import storage
from playwright.async_api import async_playwright

from .exceptions import ConfigurationError, GCSInteractionError, DiagramGenerationError


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
        raise ConfigurationError("GOOGLE_CLOUD_STORAGE_BUCKET environment variable not set.")

    # Convert escaped newlines and quotes from the JSON string back to their literal versions
    processed_mermaid_code = mermaid_code.replace('\\n', '\n').replace('\\"', '"')

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

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html_template)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                diagram_element = page.locator(".mermaid")
                await diagram_element.screenshot(path=tmp_file.name)
                tmp_file_path = tmp_file.name

            await browser.close()
    except Exception as e:
        raise DiagramGenerationError(f"Error during Playwright rendering: {e}")

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # Get the base name of the file, stripping any extension
        base_name, _ = os.path.splitext(file_name)
        # Construct the destination path with a single, correct .png extension
        destination_blob_name = f"diagrams/{base_name}.png"
        
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(tmp_file_path)
        os.remove(tmp_file_path)

        print(f"INFO: Diagram uploaded to gs://{bucket_name}/{destination_blob_name}")
        # Make the blob public to get a URL.
        # Note: In production, you would use signed URLs for security.
        blob.make_public()
        return blob.public_url
    except Exception as e:
        raise GCSInteractionError(f"Failed to upload diagram to GCS. Details: {e}")
    

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