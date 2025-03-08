#!/bin/bash
set -e

# This script is used to build the CV from the template and data files
python3 latex_jinja_applier.py --template cv.tex.j2 --context data.yml --output cv.tex

# Simple build process working in the root directory
pdflatex -interaction=nonstopmode cv
bibtex pub
bibtex diss
bibtex tr
pdflatex -interaction=nonstopmode cv
pdflatex -interaction=nonstopmode cv

echo "Build complete. PDF is cv.pdf"