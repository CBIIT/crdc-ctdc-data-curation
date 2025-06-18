# System Design Document: Data Curation File Management

## Overview of Solution
The solution consists of two main components to handle CMB-derived data files:
1. A file renaming system to standardize file names according to CTDC conventions and copy them to a specified output directory
2. A manifest generation system to create file transfer manifests with required metadata

```mermaid
graph TB
    subgraph File Processing
        A[Input Files] --> B[File Renamer]
        B --> |Copy to| O[Output Directory]
        O --> C[Renamed Files]
    end
    
    subgraph Manifest Generation
        C --> D[Manifest Generator]
        D --> E[File Metadata Extractor]
        E --> F[Checksum Calculator]
        F --> G[Transfer Manifest]
    end

```

### Module Tree
```
src/
├── file_management/
│   ├── __init__.py
│   ├── file_renamer.py
│   └── checksum.py
├── manifest/
│   ├── __init__.py
│   ├── manifest_generator.py
│   └── metadata_extractor.py
└── utils/
    ├── __init__.py
    └── file_utils.py
```

## Module Specifications

### 1. file_renamer.py
- **Name**: file_renamer.py
- **Purpose**: Handles the renaming of CMB data files according to CTDC naming conventions and manages file copying to output directory
- **Dependencies**:
  - os
  - pathlib
  - logging
  - re
  - shutil

#### Functions/Classes:
```mermaid
classDiagram
    class FileRenamer {
        +rename_vcf_file(file_path: Path) str
        +rename_pdf_file(file_path: Path) str
        +rename_and_copy(file_path: Path, output_dir: Path, dry_run: bool) tuple[str, Path]
        -_validate_filename(filename: str) bool
        -_extract_specimen_id(filename: str) str
    }
```

- **FileRenamer**
  - rename_vcf_file(file_path: Path) → str
    - Renames VCF files according to pattern "MSB-XXXXX-XX-somatic-mutations-CTDCv1.vcf"
  - rename_pdf_file(file_path: Path) → str
    - Renames PDF files according to pattern "MSB-XXXXX-XX-genomic-report-CTDCv1.pdf"
  - rename_and_copy(file_path: Path, output_dir: Path, dry_run: bool) → tuple[str, Path]
    - Renames a file according to CTDC conventions and copies it to the output directory
    - Returns tuple of (new_filename, new_file_path)
    - If dry_run is True, only returns the new name without copying

**Existing or New**: New module

### 2. manifest_generator.py
- **Name**: manifest_generator.py
- **Purpose**: Generates file transfer manifests with required metadata for each file type
- **Dependencies**:
  - pandas
  - pathlib
  - metadata_extractor
  - checksum

#### Functions/Classes:
```mermaid
classDiagram
    class ManifestGenerator {
        +generate_manifest(input_dir: Path, output_path: Path) DataFrame
        -_process_somatic_mutations(files: List[Path]) List[Dict]
        -_process_genomic_reports(files: List[Path]) List[Dict]
        -_process_clinical_reports(files: List[Path]) List[Dict]
    }
```

- **ManifestGenerator**
  - generate_manifest(input_dir: Path, output_path: Path) → DataFrame
    - Creates transfer manifest for all files with required metadata fields

**Existing or New**: New module

### 3. metadata_extractor.py
- **Name**: metadata_extractor.py
- **Purpose**: Extracts and validates metadata from filenames and file contents
- **Dependencies**:
  - pathlib
  - re

#### Functions/Classes:
```mermaid
classDiagram
    class MetadataExtractor {
        +extract_specimen_id(filename: str) str
        +extract_subject_id(filename: str) str
        +get_file_metadata(file_path: Path) Dict
    }
```

- **MetadataExtractor**
  - extract_specimen_id(filename: str) → str
    - Extracts specimen ID from filename (first 13 characters)
  - get_file_metadata(file_path: Path) → Dict
    - Returns complete metadata dictionary for a file

**Existing or New**: New module

### 4. checksum.py
- **Name**: checksum.py
- **Purpose**: Calculates file checksums and sizes
- **Dependencies**:
  - hashlib
  - pathlib

#### Functions/Classes:
```mermaid
classDiagram
    class ChecksumCalculator {
        +calculate_md5(file_path: Path) str
        +get_file_size(file_path: Path) int
    }
```

- **ChecksumCalculator**
  - calculate_md5(file_path: Path) → str
    - Calculates MD5 checksum of file
  - get_file_size(file_path: Path) → int
    - Returns file size in bytes

**Existing or New**: New module

## Module Interaction Diagram
```mermaid
sequenceDiagram
    participant Main
    participant FileRenamer
    participant ManifestGenerator 
    participant MetadataExtractor
    participant ChecksumCalculator

    Main->>FileRenamer: Process files with output dir
    FileRenamer->>FileRenamer: Validate & rename
    FileRenamer->>FileRenamer: Copy to output dir
    FileRenamer-->>Main: Renamed files in output dir
    Main->>ManifestGenerator: Generate manifest
    ManifestGenerator->>MetadataExtractor: Extract metadata
    MetadataExtractor-->>ManifestGenerator: File metadata
    ManifestGenerator->>ChecksumCalculator: Calculate checksums
    ChecksumCalculator-->>ManifestGenerator: File checksums
    ManifestGenerator-->>Main: Complete manifest
```

## Error Handling and Logging
- All modules will use Python's built-in logging module
- File operations will have proper try-except blocks
- Input validation for filenames and metadata
- Checksum verification after file operations
- Manifest data validation before writing

## Best Practices
- Type hints used throughout the codebase
- PEP 8 style guidelines followed
- Docstrings for all modules, classes, and functions
- Unit tests for each module
- Configuration stored in separate config files
- Modular design for easy maintenance and extension
