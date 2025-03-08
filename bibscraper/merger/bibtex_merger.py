"""
BibTeX merger for combining entries from multiple sources.
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from bibscraper.merger.similarity import calculate_similarity, get_entry_signature, merge_entries
from bibscraper.utils.bibtex import extract_citation_key, read_bibtex_file

# Configure logging
logger = logging.getLogger(__name__)


class BibTeXMerger:
    """
    Merger for BibTeX files.
    """
    
    def __init__(self, similarity_threshold: float = 0.8, verbose: bool = False):
        """
        Initialize a BibTeX merger.
        
        Args:
            similarity_threshold: Threshold for entry similarity (0.0-1.0)
            verbose: Enable verbose output
        """
        self.similarity_threshold = similarity_threshold
        if verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    
    def merge_files(self, file1: Path, file2: Path, output_file: Path) -> Dict[str, str]:
        """
        Merge two BibTeX files, handling duplicate entries.
        
        Args:
            file1: First BibTeX file
            file2: Second BibTeX file
            output_file: Path to write the merged BibTeX
            
        Returns:
            Dictionary of merged entries by citation key
        """
        # Read entries from both files
        logger.info(f"Reading {file1}...")
        entries1 = read_bibtex_file(file1)
        
        logger.info(f"Reading {file2}...")
        entries2 = read_bibtex_file(file2)
        
        logger.info(f"File 1 has {len(entries1)} entries")
        logger.info(f"File 2 has {len(entries2)} entries")
        
        # Merge the entries
        merged_entries = self.merge_entries(entries1, entries2)
        
        # Write merged entries to output file
        logger.info(f"Writing merged BibTeX to {output_file}...")
        with output_file.open('w', encoding='utf-8') as f:
            for entry in merged_entries.values():
                f.write(entry + "\n\n")
        
        return merged_entries
    
    def merge_entries(self, entries1: Dict[str, str], entries2: Dict[str, str]) -> Dict[str, str]:
        """
        Merge two sets of BibTeX entries.
        
        Args:
            entries1: First set of entries
            entries2: Second set of entries
            
        Returns:
            Merged entries
        """
        # Start with entries from the first set
        merged_entries = dict(entries1)
        
        # Track matches and new entries
        matches = 0
        new_entries = 0
        
        # Create a dictionary of signatures for faster matching
        signatures1 = {get_entry_signature(entry): key for key, entry in entries1.items()}
        
        # Process entries from the second set
        for key2, entry2 in entries2.items():
            # Skip if the key already exists in entries1 (direct key match)
            if key2 in merged_entries:
                logger.debug(f"Direct key match: {key2}")
                merged_entries[key2] = merge_entries(merged_entries[key2], entry2)
                matches += 1
                continue
            
            # Try matching by signature
            sig2 = get_entry_signature(entry2)
            if sig2 in signatures1:
                key1 = signatures1[sig2]
                logger.debug(f"Signature match: {key1} with {key2}")
                merged_entries[key1] = merge_entries(merged_entries[key1], entry2)
                matches += 1
                continue
            
            # Try content-based matching
            best_match = None
            best_similarity = 0.0
            
            for key1, entry1 in merged_entries.items():
                similarity = calculate_similarity(entry1, entry2)
                if similarity > self.similarity_threshold and similarity > best_similarity:
                    best_similarity = similarity
                    best_match = key1
            
            if best_match:
                logger.debug(f"Content match: {best_match} with {key2} (similarity: {best_similarity:.3f})")
                merged_entries[best_match] = merge_entries(merged_entries[best_match], entry2)
                matches += 1
            else:
                # No match found, add as new entry
                logger.debug(f"New entry: {key2}")
                merged_entries[key2] = entry2
                new_entries += 1
        
        logger.info(f"Matches found: {matches}")
        logger.info(f"New entries added: {new_entries}")
        logger.info(f"Total entries in merged file: {len(merged_entries)}")
        
        return merged_entries


def merge_bibtex_files(
    file1: Path,
    file2: Path,
    output_file: Path,
    similarity_threshold: float = 0.8,
    verbose: bool = False
) -> Dict[str, str]:
    """
    Merge two BibTeX files and save the result.
    
    Args:
        file1: Path to first BibTeX file
        file2: Path to second BibTeX file
        output_file: Path to write merged result
        similarity_threshold: Threshold for entry similarity (0.0-1.0)
        verbose: Enable verbose output
        
    Returns:
        Dictionary of merged entries by citation key
    """
    merger = BibTeXMerger(similarity_threshold, verbose)
    return merger.merge_files(file1, file2, output_file)