#!/bin/bash
set -e

# This script is used to build the CV from the template and data files
python3 latex_jinja_applier.py --template cv.tex.j2 --context data.yml --output cv.tex

# macro pdflatex with pedantic compilation to catch errors
function makepdf {
    command pdflatex -halt-on-error -interaction=nonstopmode -file-line-error $1
    if grep -q "LaTeX Error" ${1%.*}.log; then
        echo "Error in $1"
        exit 1
    fi
}

# Simple build process working in the root directory
makepdf cv.tex
bibtex pub
bibtex diss
bibtex tr

# in all .bbl files generated, replace Nikolaos Kyriazis with \textbf{Nikolaos Kyriazis}
sed -i 's/Nikolaos Kyriazis/\\textbf{Nikolaos Kyriazis}/g' pub.bbl
sed -i 's/Nikolaos Kyriazis/\\textbf{Nikolaos Kyriazis}/g' diss.bbl
sed -i 's/Nikolaos Kyriazis/\\textbf{Nikolaos Kyriazis}/g' tr.bbl

makepdf cv.tex
makepdf cv.tex

echo "Build complete. PDF is cv.pdf"