"""
Module for calculating file checksums and sizes.
"""
import hashlib
from pathlib import Path

class ChecksumCalculator:
    """Class for calculating file checksums and sizes."""

    def calculate_md5(self, file_path: Path) -> str:
        """
        Calculates MD5 checksum of file.

        Args:
            file_path (Path): Path to the file

        Returns:
            str: MD5 checksum as hexadecimal string

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_file_size(self, file_path: Path) -> int:
        """
        Returns file size in bytes.

        Args:
            file_path (Path): Path to the file

        Returns:
            int: File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        return file_path.stat().st_size
