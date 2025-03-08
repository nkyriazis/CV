"""
Command-line interfaces for BibScraper tools.
"""

import logging
import sys
from pathlib import Path

from clize import run

from bibscraper.merger.bibtex_merger import merge_bibtex_files
from bibscraper.scraper.web import scrape_from_url
from bibscraper.updater import update_bibliography

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def scrape_cli(*, url: str, output: str, verbose: bool = False):
    """
    Scrape BibTeX entries from a webpage.

    :param url: URL of the webpage containing BibTeX entries
    :param output: Path to save the scraped entries
    :param verbose: Enable verbose output
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        entries = scrape_from_url(url, Path(output))
        return 0
    except Exception as e:
        logger.error(f"Error scraping entries: {e}")
        return 1


def merge_cli(
    *,
    file1: str,
    file2: str,
    output: str,
    similarity_threshold: float = 0.8,
    verbose: bool = False,
):
    """
    Merge BibTeX files.

    :param file1: Path to the first BibTeX file
    :param file2: Path to the second BibTeX file
    :param output: Path to save the merged entries
    :param similarity_threshold: Threshold for entry similarity (0.0-1.0)
    :param verbose: Enable verbose output
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        merge_bibtex_files(
            Path(file1), Path(file2), Path(output), similarity_threshold, verbose
        )
        return 0
    except Exception as e:
        logger.error(f"Error merging files: {e}")
        return 1


def update_cli(
    *,
    new_entries: str,
    output: str,
    existing: str = None,
    source_url: str = "https://users.ics.forth.gr/~argyros/publications.html",
    title: str = "Bibliography",
    verbose: bool = False,
):
    """
    Update bibliography with changelog.

    :param new_entries: Path to new BibTeX entries
    :param output: Path to write updated bibliography
    :param existing: Path to existing bibliography (optional)
    :param source_url: URL of the source for the bibliography
    :param title: Title for the bibliography
    :param verbose: Enable verbose output
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        update_bibliography(
            Path(existing) if existing else None,
            Path(new_entries),
            Path(output),
            source_url,
            title,
            verbose,
        )
        return 0
    except Exception as e:
        logger.error(f"Error updating bibliography: {e}")
        return 1


def main_scrape():
    """Entry point for bib-scrape command."""
    sys.exit(run(scrape_cli))


def main_merge():
    """Entry point for bib-merge command."""
    sys.exit(run(merge_cli))


def main_update():
    """Entry point for bib-update command."""
    sys.exit(run(update_cli))
