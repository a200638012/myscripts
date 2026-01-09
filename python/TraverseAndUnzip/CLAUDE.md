# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TraverseAndUnzip is a Python utility script that traverses a directory to find all zip files, unzips them to their respective locations, and generates a report of the operation.

## Architecture

The project consists of a single main script `TraverseAndUnzip.py` that implements the following workflow:

1. **Input**: Accepts a directory path as input
2. **Traversal**: Recursively walks through the directory tree to find all zip files
3. **Documentation**: Creates a file tree listing all discovered zip files in `report/{dirname}.md`
4. **Extraction**: Unzips each file to its containing directory (preserving the original structure)
5. **Reporting**: Generates a final report showing the correspondence between zipped and unzipped files

## Running the Script

The script is intended to be run directly with Python 3.x:

```bash
python TraverseAndUnzip.py
```

The script will prompt for a directory path when executed.

## Development Notes

- Python 3.13.2 is the current runtime environment
- Uses only standard library modules: `zipfile` and `os`
- The `report/` directory is created dynamically if it doesn't exist
- Zip files are extracted in-place (unzipped contents go into the same directory as the zip file)
