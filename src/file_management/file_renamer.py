"""
Module for handling the renaming of CMB data files according to CTDC naming conventions.
"""
import os
from pathlib import Path
import logging
import re

class FileRenamer:
    """Class for renaming files according to CTDC naming conventions."""

    def rename_vcf_file(self, file_path: Path) -> str:
        """
        Renames VCF files according to pattern "MSB-XXXXX-XX-somatic-mutations-CTDCv1.vcf"

        Args:
            file_path (Path): Path to the VCF file to be renamed

        Returns:
            str: New filename

        Raises:
            ValueError: If the filename is invalid or cannot be processed
        """
        if not self._validate_filename(file_path.name):
            raise ValueError(f"Invalid filename format: {file_path.name}")

        specimen_id = self._extract_specimen_id(file_path.name)
        new_name = f"{specimen_id}-somatic-mutations-CTDCv1.vcf"
        return new_name

    def rename_pdf_file(self, file_path: Path) -> str:
        """
        Renames PDF files according to pattern "MSB-XXXXX-XX-genomic-report-CTDCv1.pdf"

        Args:
            file_path (Path): Path to the PDF file to be renamed

        Returns:
            str: New filename

        Raises:
            ValueError: If the filename is invalid or cannot be processed
        """
        if not self._validate_filename(file_path.name):
            raise ValueError(f"Invalid filename format: {file_path.name}")

        specimen_id = self._extract_specimen_id(file_path.name)
        new_name = f"{specimen_id}-genomic-report-CTDCv1.pdf"
        return new_name

    def _validate_filename(self, filename: str) -> bool:
        """
        Validates if the filename matches the expected format.

        Args:
            filename (str): Name of the file to validate

        Returns:
            bool: True if valid, False otherwise
        """
        # Expected format: MSB-XXXXX-XX followed by additional text
        pattern = r'^MSB-\d{5}-\d{2}'
        return bool(re.match(pattern, filename))

    def _extract_specimen_id(self, filename: str) -> str:
        """
        Extracts the specimen ID from the filename.

        Args:
            filename (str): Name of the file

        Returns:
            str: Extracted specimen ID (first 13 characters)

        Raises:
            ValueError: If specimen ID cannot be extracted
        """
        specimen_id = filename[:13]  # Extract first 13 characters (MSB-XXXXX-XX)
        if not re.match(r'^MSB-\d{5}-\d{2}$', specimen_id):
            raise ValueError(f"Could not extract valid specimen ID from: {filename}")
        return specimen_id
