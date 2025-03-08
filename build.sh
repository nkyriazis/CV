#!/bin/bash

# Simple build process working in the root directory
pdflatex cv
bibtex pub
bibtex diss
bibtex tr
pdflatex cv
pdflatex cv

echo "Build complete. PDF is cv.pdf"