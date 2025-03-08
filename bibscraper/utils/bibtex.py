"""
Utility functions for working with BibTeX files.
"""
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def extract_citation_key(entry: str) -> Optional[str]:
    """
    Extract the citation key from a BibTeX entry.
    For example, from "@article{Smith2021, ...}" extract "Smith2021".
    
    Args:
        entry: A BibTeX entry string
        
    Returns:
        The citation key or None if not found
    """
    match = re.match(r'@[a-zA-Z]+\s*\{([^,]*)', entry)
    if match:
        return match.group(1).strip()
    return None


def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace and converting to lowercase.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    return re.sub(r'\s+', ' ', text).strip().lower()


def extract_field(entry: str, field: str) -> Optional[str]:
    """
    Extract a field from a BibTeX entry.
    
    Args:
        entry: A BibTeX entry string
        field: The field name to extract (e.g., 'title', 'author')
        
    Returns:
        The field value or None if not found
    """
    pattern = fr'{field}\s*=\s*\{{(.*?)\}}|{field}\s*=\s*"(.*?)"'
    match = re.search(pattern, entry, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1) or match.group(2)
    return None


def count_entries(bib_file: Path) -> int:
    """
    Count the number of BibTeX entries in a file.
    
    Args:
        bib_file: Path to a BibTeX file
        
    Returns:
        Number of entries
    """
    if not bib_file.exists():
        return 0
    
    content = bib_file.read_text(encoding='utf-8')
    # Count @ symbols that start entries (not in comments)
    entry_count = len(re.findall(r'^@', content, re.MULTILINE))
    return entry_count


def extract_entries(content: str) -> List[str]:
    """
    Extract BibTeX entries from text content.
    
    Args:
        content: Text containing BibTeX entries
        
    Returns:
        List of BibTeX entry strings
    """
    # BibTeX entries typically start with @article, @inproceedings, etc.
    # and are enclosed in curly braces
    bibtex_pattern = r'(@[a-zA-Z]+\s*\{[^@]*\})'
    entries = re.findall(bibtex_pattern, content, re.DOTALL)
    return entries


def read_bibtex_file(file_path: Path) -> Dict[str, str]:
    """
    Read a BibTeX file and return entries indexed by citation key.
    
    Args:
        file_path: Path to a BibTeX file
        
    Returns:
        Dictionary mapping citation keys to entry strings
    """
    if not file_path.exists():
        return {}
    
    content = file_path.read_text(encoding='utf-8')
    entries = extract_entries(content)
    
    result = {}
    for entry in entries:
        key = extract_citation_key(entry)
        if key:
            result[key] = entry
    
    return result


def extract_changelog(bib_file: Path) -> Tuple[List[str], str]:
    """
    Extract the changelog and entries from an existing bibliography file.
    
    Args:
        bib_file: Path to a BibTeX file with changelog
        
    Returns:
        Tuple of (changelog_lines, entries_content)
    """
    if not bib_file.exists():
        return [], ""
    
    content = bib_file.read_text(encoding='utf-8')
    
    # Check if the file has our changelog format
    if "% CHANGELOG" not in content:
        # No changelog, treat the whole file as entries
        return [], content
    
    # Split at the BEGIN ENTRIES marker
    parts = content.split("% BEGIN ENTRIES", 1)
    if len(parts) != 2:
        # Malformed file, treat the whole file as entries
        return [], content
    
    # Extract the changelog lines (skip metadata lines)
    header = parts[0]
    changelog_lines = [
        line for line in header.splitlines()
        if line.startswith("% ") and not line.startswith("% BIBLIOGRAPHY") 
        and not line.startswith("% Source") and not line.startswith("% CHANGELOG")
    ]
    
    # Extract just the entries
    entries = parts[1].strip()
    
    return changelog_lines, entries