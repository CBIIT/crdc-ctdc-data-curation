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
        specimen_id = filename[:12]  # Extract first 13 characters (MSB-XXXXX-XX)
        if not re.match(r'^MSB-\d{5}-\d{2}$', specimen_id):
            raise ValueError(f"Could not extract valid specimen ID from: {filename}")
        return specimen_id

    def rename_and_copy(self, file_path: Path, output_dir: Path, dry_run: bool = False) -> tuple[str, Path]:
        """
        Renames a file according to CTDC conventions and copies it to the output directory.

        Args:
            file_path (Path): Path to the file to be renamed
            output_dir (Path): Directory where the renamed file should be saved
            dry_run (bool): If True, only return the new name without copying

        Returns:
            tuple[str, Path]: Tuple of (new_filename, new_file_path)

        Raises:
            ValueError: If the file cannot be renamed or copied
        """
        # Get new filename based on file type
        if file_path.suffix.lower() == '.vcf':
            new_name = self.rename_vcf_file(file_path)
        elif file_path.suffix.lower() == '.pdf':
            new_name = self.rename_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        new_path = output_dir / new_name

        if not dry_run:
            import shutil
            try:
                shutil.copy2(file_path, new_path)
            except Exception as e:
                raise ValueError(f"Failed to copy file {file_path} to {new_path}: {e}")

        return new_name, new_path
