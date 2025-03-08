"""
Bibliography updater with changelog.
"""
import logging
import tempfile
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bibscraper.merger.bibtex_merger import BibTeXMerger
from bibscraper.utils.bibtex import count_entries, extract_changelog
from bibscraper.utils.changelog import create_changelog_entry, create_bibliography_with_changelog

# Configure logging
logger = logging.getLogger(__name__)


class BibliographyUpdater:
    """
    Updates a bibliography with new entries and maintains a changelog.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize a bibliography updater.
        
        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        if verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    
    def update(
        self,
        existing_bib: Optional[Path],
        new_entries_bib: Path,
        output_bib: Path,
        source_url: str,
        title: str = "Bibliography"
    ) -> None:
        """
        Update bibliography with new entries and maintain changelog.
        
        Args:
            existing_bib: Path to existing bibliography or None
            new_entries_bib: Path to new entries
            output_bib: Path to write updated bibliography
            source_url: URL of the source for the bibliography
            title: Title for the bibliography
        """
        today = datetime.now()
        new_entries_count = count_entries(new_entries_bib)
        
        # Check if we have an existing bibliography
        if existing_bib and existing_bib.exists():
            # Extract changelog and entries from existing bibliography
            changelog_lines, existing_entries = extract_changelog(existing_bib)
            
            # Create temporary files for the merger
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.bib', delete=False) as temp_file:
                temp_existing = Path(temp_file.name)
                temp_file.write(existing_entries)
            
            # Create temporary output file
            merged_entries = Path(tempfile.mktemp(suffix='.bib'))
            
            # Merge the files
            merger = BibTeXMerger(verbose=self.verbose)
            merger.merge_files(temp_existing, new_entries_bib, merged_entries)
            
            # Count entries in the merged file
            merged_count = count_entries(merged_entries)
            new_added = merged_count - count_entries(temp_existing)
            
            # Add new changelog entry if there are new entries
            if new_added > 0:
                changelog_entry = create_changelog_entry(
                    today, merged_count, new_added, first_scrape=False
                )
                changelog_lines.insert(0, changelog_entry)
            
            # Read the merged entries
            merged_content = merged_entries.read_text(encoding='utf-8')
            
            # Clean up temporary files
            temp_existing.unlink()
            merged_entries.unlink()
        else:
            # No existing bibliography, create a new one
            changelog_entry = create_changelog_entry(
                today, new_entries_count, 0, first_scrape=True
            )
            changelog_lines = [changelog_entry]
            merged_content = new_entries_bib.read_text(encoding='utf-8')
        
        # Create the complete bibliography with changelog
        bibliography = create_bibliography_with_changelog(
            merged_content, changelog_lines, source_url, title
        )
        
        # Write the output file
        output_bib.write_text(bibliography, encoding='utf-8')
        
        logger.info(f"Bibliography updated with {count_entries(output_bib)} entries")
        logger.info(f"Changelog updated with {len(changelog_lines)} entries")


def update_bibliography(
    existing_bib: Optional[Path],
    new_entries_bib: Path,
    output_bib: Path,
    source_url: str,
    title: str = "Bibliography",
    verbose: bool = False
) -> None:
    """
    Update a bibliography with new entries and maintain a changelog.
    
    Args:
        existing_bib: Path to existing bibliography or None
        new_entries_bib: Path to new entries
        output_bib: Path to write updated bibliography
        source_url: URL of the source for the bibliography
        title: Title for the bibliography
        verbose: Enable verbose output
    """
    updater = BibliographyUpdater(verbose=verbose)
    updater.update(existing_bib, new_entries_bib, output_bib, source_url, title)