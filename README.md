# BibScraper

A Python framework for scraping, merging, and managing BibTeX bibliographies.

## Features

- Scrape BibTeX entries from academic webpages
- Handle duplicate entries with intelligent merging algorithms
- Maintain comprehensive bibliographies with changelogs
- Easily update bibliographies with new entries
- Command-line tools for all operations

## Installation

```bash
# From source
git clone https://github.com/yourusername/bibscraper.git
cd bibscraper
pip install .

# Or directly from PyPI (once published)
# pip install bibscraper
```

## Usage

### Command Line Tools

#### Scraping BibTeX entries

```bash
bib-scrape --url "https://users.ics.forth.gr/~argyros/publications.html" --output argyros.bib
```

#### Merging BibTeX files

```bash
bib-merge --file1 first.bib --file2 second.bib --output merged.bib --similarity-threshold 0.8 --verbose
```

#### Updating a bibliography with changelog

```bash
bib-update --existing bibliography.bib --new-entries new_entries.bib --output updated.bib --source-url "https://example.com/publications"
```

### Python API

```python
from pathlib import Path
from bibscraper.scraper.web import scrape_from_url
from bibscraper.merger.bibtex_merger import merge_bibtex_files
from bibscraper.updater import update_bibliography

# Scrape BibTeX entries
entries = scrape_from_url(
    "https://users.ics.forth.gr/~argyros/publications.html",
    Path("argyros.bib")
)

# Merge BibTeX files
merge_bibtex_files(
    Path("first.bib"),
    Path("second.bib"),
    Path("merged.bib"),
    similarity_threshold=0.8,
    verbose=True
)

# Update bibliography with changelog
update_bibliography(
    Path("bibliography.bib"),
    Path("new_entries.bib"),
    Path("updated.bib"),
    "https://example.com/publications",
    "My Bibliography"
)
```

## Output Format

The bibliography file includes a changelog in BibTeX comments:

```bibtex
% Bibliography
% Source: https://example.com/publications
%
% CHANGELOG
% 2025-03-08: 292 total entries (first scrape)
% 2025-04-01: 295 total entries (+3 new)
% BEGIN ENTRIES

@inproceedings{Gouidis2025wacv,
  author = {Filippos Gouidis and Konstantinos Papoutsakis and Theodore Patkos and Antonis Argyros and Dimitris Plexousakis},
  title = {Recognizing Unseen States of Unknown Objects by Leveraging Knowledge Graphs},
  booktitle = {IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2025)},
  year = {2025},
  ...
}
```

## GitHub Actions Integration

This package can be easily integrated with GitHub Actions for automated bibliography updates. See the `.github/workflows/update-bibliography.yml` file in the repository for an example workflow.

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- python-Levenshtein

## License

MIT