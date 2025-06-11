# FILE: scripts/scrape_adk_docs.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from markdownify import markdownify as md
import re

# The starting point for our scrape
BASE_URL = "https://google.github.io/adk-docs/"
OUTPUT_DIR = "data/knowledge_base/"

# Keep track of visited URLs to avoid infinite loops and redundant scrapes
visited_urls = set()

def clean_url(url):
    """Removes URL fragments and query parameters to avoid duplicate pages."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".strip('/')

def scrape_page(url):
    """
    Scrapes a single page, converts its main content to Markdown, and finds new links.
    """
    # Normalize the URL to avoid scraping the same page with different fragments
    normalized_url = clean_url(url)
    if normalized_url in visited_urls:
        return []
    
    print(f"Scraping: {url}")
    visited_urls.add(normalized_url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  ERROR: Could not fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    
    # This selector is specific to the ADK docs site structure.
    # It targets the main content area of the page.
    content_area = soup.select_one(".md-content .md-content__inner")

    if content_area:
        # Get the page title for context
        title_tag = soup.find("title")
        page_title = title_tag.get_text().replace(" - ADK", "").strip() if title_tag else "ADK Document"

        # Convert the HTML content directly to Markdown
        # This preserves headings, lists, code blocks, etc.
        markdown_content = md(str(content_area), heading_style="ATX")
        
        # --- Post-processing the Markdown for cleaner output ---
        # Remove extra blank lines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        # Add a title and source URL to the top of the file for context
        final_content = f"# {page_title}\n\n**Source URL:** {url}\n\n---\n\n{markdown_content}"
        
        # Generate a clean filename from the URL path
        path = urlparse(url).path
        filename = path.strip('/').replace('/', '_').replace('.html', '') or "index"
        filename = os.path.join(OUTPUT_DIR, f"{filename}.md")
        
        # Save the content
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"  -> Saved to {filename}")

    # Find all links on the page that point to other docs pages
    new_links = []
    # Target links within the main navigation and content area
    for link in soup.select(".md-nav__link, .md-content a"):
        if 'href' not in link.attrs:
            continue
            
        href = link['href']
        # Construct absolute URL for relative links
        absolute_url = urljoin(BASE_URL, href)
        
        # Follow links only if they are within the same documentation site
        if absolute_url.startswith(BASE_URL):
            normalized_new_link = clean_url(absolute_url)
            if normalized_new_link not in visited_urls:
                new_links.append(absolute_url)
                
    return new_links

def run_scraper():
    """Main function to run the web scraper."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # Start with the base URL and expand from there
    urls_to_scrape = [BASE_URL]
    
    while urls_to_scrape:
        current_url = urls_to_scrape.pop(0)
        # Use a list and set to get unique new links
        new_links = list(set(scrape_page(current_url)))
        
        for link in new_links:
            if clean_url(link) not in visited_urls:
                 urls_to_scrape.append(link)
    
    print("\n✅ Scraping complete.")
    print(f"Total unique pages scraped: {len(visited_urls)}")

if __name__ == "__main__":
    run_scraper()