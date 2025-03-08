"""
Utilities for managing bibliography changelogs.
"""
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from bibscraper.utils.bibtex import extract_changelog


def create_changelog_entry(
    date: datetime,
    total_entries: int,
    new_entries: int,
    first_scrape: bool = False
) -> str:
    """
    Create a changelog entry for a bibliography update.
    
    Args:
        date: Date of the update
        total_entries: Total number of entries after update
        new_entries: Number of new entries added
        first_scrape: Whether this is the first scrape
        
    Returns:
        Formatted changelog entry
    """
    date_str = date.strftime("%Y-%m-%d")
    
    if first_scrape:
        return f"% {date_str}: {total_entries} total entries (first scrape)"
    else:
        return f"% {date_str}: {total_entries} total entries (+{new_entries} new)"


def create_bibliography_with_changelog(
    entries_content: str,
    changelog_lines: List[str],
    source_url: str,
    title: str = "Bibliography"
) -> str:
    """
    Create a BibTeX file with a changelog.
    
    Args:
        entries_content: BibTeX entry content
        changelog_lines: List of changelog lines
        source_url: URL of the source
        title: Title for the bibliography
        
    Returns:
        Complete bibliography content with changelog
    """
    content = [
        f"% {title}",
        f"% Source: {source_url}",
        "%",
        "% CHANGELOG"
    ]
    
    # Add changelog entries
    for line in changelog_lines:
        content.append(line)
    
    content.append("% BEGIN ENTRIES")
    content.append("")  # Empty line before entries
    content.append(entries_content)
    
    return "\n".join(content)