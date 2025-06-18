"""
Tests for file utility functions.
"""
import os
from pathlib import Path
import pytest
from src.utils.file_utils import ensure_directory, safe_file_move, list_files_by_extension

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    return test_dir

def test_ensure_directory(temp_dir):
    """Test ensuring directory exists."""
    new_dir = temp_dir / "new_dir"
    ensure_directory(new_dir)
    assert new_dir.exists()
    assert new_dir.is_dir()

def test_ensure_nested_directory(temp_dir):
    """Test ensuring nested directory exists."""
    nested_dir = temp_dir / "parent" / "child" / "grandchild"
    ensure_directory(nested_dir)
    assert nested_dir.exists()
    assert nested_dir.is_dir()

def test_safe_file_move(temp_dir):
    """Test safe file movement."""
    source = temp_dir / "source.txt"
    dest = temp_dir / "subdir" / "dest.txt"
    source.write_text("test content")

    safe_file_move(source, dest)
    
    assert not source.exists()
    assert dest.exists()
    assert dest.read_text() == "test content"

def test_safe_file_move_nonexistent_source(temp_dir):
    """Test safe file movement with nonexistent source."""
    source = temp_dir / "nonexistent.txt"
    dest = temp_dir / "dest.txt"

    with pytest.raises(FileNotFoundError):
        safe_file_move(source, dest)

def test_list_files_by_extension(temp_dir):
    """Test listing files by extension."""
    # Create test files
    (temp_dir / "test1.txt").write_text("test1")
    (temp_dir / "test2.txt").write_text("test2")
    (temp_dir / "test.pdf").write_text("test pdf")
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    (subdir / "test3.txt").write_text("test3")

    # Test finding .txt files
    txt_files = list_files_by_extension(temp_dir, ".txt")
    assert len(txt_files) == 3
    assert all(f.suffix == ".txt" for f in txt_files)

    # Test finding .pdf files
    pdf_files = list_files_by_extension(temp_dir, ".pdf")
    assert len(pdf_files) == 1
    assert pdf_files[0].name == "test.pdf"

def test_list_files_by_extension_nonexistent_dir():
    """Test listing files with nonexistent directory."""
    with pytest.raises(FileNotFoundError):
        list_files_by_extension(Path("/nonexistent"), ".txt")
