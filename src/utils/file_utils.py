"""
Utility functions for file operations.
"""
import os
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)

def ensure_directory(path: Path) -> None:
    """
    Ensures a directory exists, creates it if it doesn't.

    Args:
        path (Path): Directory path to ensure exists

    Raises:
        OSError: If directory cannot be created
    """
    path.mkdir(parents=True, exist_ok=True)

def safe_file_move(source: Path, dest: Path) -> None:
    """
    Safely moves a file from source to destination.

    Args:
        source (Path): Source file path
        dest (Path): Destination file path

    Raises:
        FileNotFoundError: If source file doesn't exist
        OSError: If file cannot be moved
    """
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    
    ensure_directory(dest.parent)
    os.replace(source, dest)

def list_files_by_extension(directory: Path, extension: str) -> List[Path]:
    """
    Lists all files with given extension in directory.

    Args:
        directory (Path): Directory to search
        extension (str): File extension to match (e.g., '.pdf')

    Returns:
        List[Path]: List of matching file paths

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    return list(directory.glob(f"**/*{extension}"))
