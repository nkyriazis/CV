"""
Similarity-based BibTeX entry matching and merging.
"""
import re
from typing import Dict, List, Optional, Tuple

import Levenshtein

from bibscraper.utils.bibtex import extract_field, normalize_text


def get_entry_signature(entry: str) -> str:
    """
    Generate a signature for an entry based on its key fields.
    
    Args:
        entry: A BibTeX entry string
        
    Returns:
        A signature string derived from the entry's content
    """
    title = extract_field(entry, 'title') or ''
    author = extract_field(entry, 'author') or ''
    year = extract_field(entry, 'year') or ''
    doi = extract_field(entry, 'doi') or ''
    
    # If DOI exists, it's a reliable identifier
    if doi:
        return f"doi:{normalize_text(doi)}"
    
    # Otherwise combine author, title, and year
    return (
        f"title:{normalize_text(title)}|"
        f"author:{normalize_text(author)}|"
        f"year:{year}"
    )


def calculate_similarity(entry1: str, entry2: str) -> float:
    """
    Calculate similarity between two BibTeX entries.
    
    Args:
        entry1: First BibTeX entry
        entry2: Second BibTeX entry
        
    Returns:
        Similarity score between 0 and 1
    """
    # Extract and normalize key fields
    title1 = normalize_text(extract_field(entry1, 'title') or '')
    title2 = normalize_text(extract_field(entry2, 'title') or '')
    
    author1 = normalize_text(extract_field(entry1, 'author') or '')
    author2 = normalize_text(extract_field(entry2, 'author') or '')
    
    year1 = extract_field(entry1, 'year') or ''
    year2 = extract_field(entry2, 'year') or ''
    
    # Calculate similarity scores for each field
    title_sim = Levenshtein.ratio(title1, title2) if title1 and title2 else 0
    author_sim = Levenshtein.ratio(author1, author2) if author1 and author2 else 0
    year_sim = 1.0 if year1 and year2 and year1 == year2 else 0
    
    # Apply weights to each field
    total_weight = 0.0
    weighted_sim = 0.0
    
    if title1 and title2:
        weighted_sim += title_sim * 0.5
        total_weight += 0.5
    
    if author1 and author2:
        weighted_sim += author_sim * 0.3
        total_weight += 0.3
    
    if year1 and year2:
        weighted_sim += year_sim * 0.2
        total_weight += 0.2
    
    # Calculate final score, normalized by total weights
    return weighted_sim / total_weight if total_weight > 0 else 0.0


def merge_entries(entry1: str, entry2: str) -> str:
    """
    Merge two BibTeX entries, preserving all fields.
    
    Args:
        entry1: First BibTeX entry
        entry2: Second BibTeX entry
        
    Returns:
        Merged BibTeX entry
    """
    # Extract the entry type and key from the first entry
    match = re.match(r'(@[a-zA-Z]+)\s*\{([^,]*)', entry1)
    if not match:
        return entry1
    
    entry_type = match.group(1)
    entry_key = match.group(2).strip()
    
    # Extract fields from both entries
    field_pattern = r'([a-zA-Z0-9_]+)\s*=\s*(\{.*?\}|".*?")'
    fields1 = {k.lower(): v for k, v in re.findall(field_pattern, entry1, re.DOTALL)}
    fields2 = {k.lower(): v for k, v in re.findall(field_pattern, entry2, re.DOTALL)}
    
    # Combine fields, preferring longer values
    merged_fields = {}
    for key in set(fields1.keys()).union(fields2.keys()):
        if key in fields1 and key in fields2:
            # Choose the longer value if both entries have the field
            merged_fields[key] = fields1[key] if len(fields1[key]) >= len(fields2[key]) else fields2[key]
        elif key in fields1:
            merged_fields[key] = fields1[key]
        else:
            merged_fields[key] = fields2[key]
    
    # Reconstruct the merged entry
    merged_entry = f"{entry_type}{{{entry_key},\n"
    for key, value in merged_fields.items():
        merged_entry += f"  {key} = {value},\n"
    
    # Remove the trailing comma and close the entry
    merged_entry = merged_entry.rstrip(",\n") + "\n}"
    
    return merged_entry