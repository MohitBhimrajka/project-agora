# scripts/scrape_adk_docs.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# The starting point for our scrape
BASE_URL = "https://google.github.io/adk-docs/"
OUTPUT_DIR = "data/knowledge_base/"

# Keep track of visited URLs to avoid infinite loops
visited_urls = set()

def scrape_page(url):
    """Scrapes a single page, extracts content, and finds new links."""
    if url in visited_urls:
        return []
    
    print(f"Scraping: {url}")
    visited_urls.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    
    # This selector is specific to the ADK docs site structure.
    # It targets the main content area of the page.
    content_area = soup.select_one(".md-content")

    if content_area:
        # Extract the text content
        content_text = content_area.get_text(separator='\\n', strip=True)
        
        # Generate a clean filename from the URL path
        path = urlparse(url).path
        filename = path.strip('/').replace('/', '_') or "index"
        filename = os.path.join(OUTPUT_DIR, f"{filename}.md")
        
        # Save the content
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content_text)
        print(f"  -> Saved to {filename}")

    # Find all links on the page that point to other docs pages
    new_links = []
    for link in soup.find_all("a", href=True):
        href = link['href']
        # Construct absolute URL for relative links
        absolute_url = urljoin(BASE_URL, href)
        
        # Follow links only if they are within the same documentation site
        if absolute_url.startswith(BASE_URL) and absolute_url not in visited_urls:
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
        new_links = scrape_page(current_url)
        # Add newly found, unique links to our list to be scraped
        for link in new_links:
            if link not in urls_to_scrape:
                urls_to_scrape.append(link)
    
    print("\\n✅ Scraping complete.")

if __name__ == "__main__":
    run_scraper()