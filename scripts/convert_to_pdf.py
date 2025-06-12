#!/usr/bin/env python3
"""
Script to convert all .md and .txt files from knowledge_base directory to PDF format.
"""

import os
import sys
from pathlib import Path

import markdown
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration


def convert_md_to_pdf(md_file_path, output_pdf_path):
    """Convert a Markdown file to PDF."""
    try:
        # Read the markdown file
        with open(md_file_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content, extensions=["tables", "fenced_code", "toc"]
        )

        # Add CSS styling for better PDF formatting
        css_style = """
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        h1 { font-size: 24px; }
        h2 { font-size: 20px; }
        h3 { font-size: 18px; }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        blockquote {
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 20px;
            font-style: italic;
        }
        """

        # Create full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css_style}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(output_pdf_path)
        print(f"✅ Converted {md_file_path} to {output_pdf_path}")

    except Exception as e:
        print(f"❌ Error converting {md_file_path}: {str(e)}")


def convert_txt_to_pdf(txt_file_path, output_pdf_path):
    """Convert a text file to PDF."""
    try:
        # Read the text file
        with open(txt_file_path, "r", encoding="utf-8") as f:
            txt_content = f.read()

        # Escape HTML special characters and preserve formatting
        txt_content = txt_content.replace("&", "&amp;")
        txt_content = txt_content.replace("<", "&lt;")
        txt_content = txt_content.replace(">", "&gt;")
        txt_content = txt_content.replace("\n", "<br>\n")

        # Add CSS styling for text files
        css_style = """
        body {
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            margin: 40px;
            color: #333;
            white-space: pre-wrap;
        }
        """

        # Create full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css_style}</style>
        </head>
        <body>
            {txt_content}
        </body>
        </html>
        """

        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(output_pdf_path)
        print(f"✅ Converted {txt_file_path} to {output_pdf_path}")

    except Exception as e:
        print(f"❌ Error converting {txt_file_path}: {str(e)}")


def main():
    """Main function to convert all files in knowledge_base to PDF."""
    # Define paths
    knowledge_base_dir = Path("data/knowledge_base")
    pdf_output_dir = Path("data/pdf")

    # Create output directory if it doesn't exist
    pdf_output_dir.mkdir(parents=True, exist_ok=True)

    # Get all .md and .txt files
    md_files = list(knowledge_base_dir.glob("*.md"))
    txt_files = list(knowledge_base_dir.glob("*.txt"))

    all_files = md_files + txt_files

    if not all_files:
        print("No .md or .txt files found in the knowledge_base directory.")
        return

    print(f"Found {len(all_files)} files to convert:")
    print(f"  - {len(md_files)} Markdown files")
    print(f"  - {len(txt_files)} Text files")
    print()

    # Convert each file
    for file_path in all_files:
        # Create output PDF path
        pdf_filename = file_path.stem + ".pdf"
        output_pdf_path = pdf_output_dir / pdf_filename

        # Convert based on file extension
        if file_path.suffix.lower() == ".md":
            convert_md_to_pdf(file_path, output_pdf_path)
        elif file_path.suffix.lower() == ".txt":
            convert_txt_to_pdf(file_path, output_pdf_path)

    print(f"\n🎉 Conversion complete! All PDFs saved to: {pdf_output_dir}")


if __name__ == "__main__":
    main()
