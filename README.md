
# CRDC-CTDC Data Curation Tool

A Python-based tool for curating and managing data files according to the Cancer Research Data Commons (CRDC) and Clinical Trial Data Commons (CTDC) standards. This tool helps automate the process of file renaming, metadata extraction, and manifest generation for biomarker and VCF reports.

## Features

- Automated file renaming according to CTDC naming conventions
- Metadata extraction from biomarker and VCF reports
- Manifest generation for data submission
- Checksum generation and validation
- Support for both VCF and biomarker report file types

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crdc-ctdc-data-curation.git
   cd crdc-ctdc-data-curation
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage

### Command Line Interface (CLI)

The tool provides a command-line interface with the following commands:

1. **Rename Files**
   
   Rename files according to CTDC conventions:
   ```bash
   python -m src.main rename-files /path/to/input/directory
   ```

   Options:
   - `--dry-run`: Show what would be renamed without making changes

   Example with options:
   ```bash
   python3 -m src.main rename-files --dry-run  ./data/input/VCF_Report ./data/input/VCF_Report_rename

   python3 -m src.main rename-files ./data/input/Biomarker_Report ./data/input/Biomarker_Report_rename

   python3 -m src.main generate-manifest ./data/input/VCF_Report_rename ./data/output/manifest.csv
   ```



## Project Structure

```
.
├── data/
│   ├── input/          # Place input files here
│   └── output/         # Generated files will be here
├── src/
│   ├── file_management/
│   └── manifest/
├── tests/              # Unit tests
└── README.md
```

## Running Tests

To run the tests, make sure you have pytest installed and run:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```


