"""
Web scraper for BibTeX entries.
"""
import re
from pathlib import Path
from typing import Dict, List, Set

import requests
from bs4 import BeautifulSoup

from bibscraper.utils.bibtex import extract_citation_key, extract_entries, normalize_text


class WebScraper:
    """Scraper for BibTeX entries from web pages."""
    
    def __init__(self, url: str):
        """
        Initialize a web scraper for BibTeX entries.
        
        Args:
            url: URL of the webpage containing BibTeX entries
        """
        self.url = url
    
    def scrape(self) -> Dict[str, str]:
        """
        Scrape BibTeX entries from the webpage.
        
        Returns:
            Dictionary mapping citation keys to BibTeX entries
        """
        # Fetch the webpage content
        response = requests.get(self.url)
        if response.status_code != 200:
            print(f"Failed to retrieve page: {response.status_code}")
            return {}
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content from the page
        content = soup.get_text()
        
        # Extract BibTeX entries
        entries = extract_entries(content)
        
        # Clean up entries and organize by citation key
        clean_entries: Dict[str, str] = {}
        duplicates: Set[str] = set()
        
        for entry in entries:
            # Remove extra whitespace and normalize formatting
            clean_entry = normalize_text(entry)
            
            # Extract the citation key
            key = extract_citation_key(clean_entry)
            if key:
                if key in clean_entries:
                    # Handle duplicate keys
                    if key not in duplicates:
                        print(f"WARNING: Duplicate entry with key: {key}")
                        duplicates.add(key)
                    # Make the key unique by appending a suffix
                    i = 1
                    while f"{key}_{i}" in clean_entries:
                        i += 1
                    key = f"{key}_{i}"
                
                clean_entries[key] = clean_entry
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate citation keys that were renamed")
        
        return clean_entries


def scrape_from_url(url: str, output_file: Path = None) -> Dict[str, str]:
    """
    Scrape BibTeX entries from a URL and optionally save to a file.
    
    Args:
        url: URL to scrape
        output_file: Optional path to save the scraped entries
    
    Returns:
        Dictionary mapping citation keys to BibTeX entries
    """
    scraper = WebScraper(url)
    entries = scraper.scrape()
    
    if output_file and entries:
        with output_file.open('w', encoding='utf-8') as f:
            for entry in entries.values():
                f.write(entry + "\n\n")
        print(f"Found {len(entries)} BibTeX entries and saved to {output_file}")
    
    return entries