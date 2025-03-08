#!/bin/bash

# Clean up all build artifacts
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.pdf

# Clean up the _build directory if it exists
if [ -d "_build" ]; then
  rm -rf _build
fi

echo "All build artifacts removed."