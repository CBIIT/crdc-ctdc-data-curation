"""
Module for extracting and validating metadata from filenames and file contents.
"""
from pathlib import Path
import re
from typing import Dict

class MetadataExtractor:
    """Class for extracting metadata from files."""

    def extract_specimen_id(self, filename: str) -> str:
        """
        Extracts specimen ID from filename (first 13 characters).

        Args:
            filename (str): Name of the file

        Returns:
            str: Extracted specimen ID

        Raises:
            ValueError: If specimen ID cannot be extracted
        """
        specimen_id = filename[:13]  # Extract MSB-XXXXX-XX
        if not re.match(r'^MSB-\d{5}-\d{2}$', specimen_id):
            raise ValueError(f"Invalid specimen ID format in filename: {filename}")
        return specimen_id

    def extract_subject_id(self, filename: str) -> str:
        """
        Extracts subject ID from filename (first 9 characters).

        Args:
            filename (str): Name of the file

        Returns:
            str: Extracted subject ID

        Raises:
            ValueError: If subject ID cannot be extracted
        """
        subject_id = filename[:9]  # Extract MSB-XXXXX
        if not re.match(r'^MSB-\d{5}$', subject_id):
            raise ValueError(f"Invalid subject ID format in filename: {filename}")
        return subject_id

    def get_file_metadata(self, file_path: Path) -> Dict:
        """
        Returns complete metadata dictionary for a file.

        Args:
            file_path (Path): Path to the file

        Returns:
            Dict: Dictionary containing all metadata fields

        Raises:
            ValueError: If metadata cannot be extracted
        """
        filename = file_path.name
        metadata = {
            'data_file_name': filename
        }

        # Extract IDs based on file type
        if 'clinical-report' in filename:
            metadata['subject.subject_id'] = self.extract_subject_id(filename)
        else:
            metadata['specimen.specimen_id'] = self.extract_specimen_id(filename)

        return metadata
