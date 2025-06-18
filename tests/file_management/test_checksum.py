"""
Unit tests for the ChecksumCalculator class.
"""
import pytest
from pathlib import Path
from unittest.mock import mock_open, patch
from src.file_management.checksum import ChecksumCalculator

@pytest.fixture
def calculator():
    """Fixture providing a ChecksumCalculator instance."""
    return ChecksumCalculator()

class TestChecksumCalculator:
    """Tests for the ChecksumCalculator class."""

    def test_calculate_md5_valid_file(self, calculator, tmp_path):
        """Test MD5 calculation with a valid file."""
        test_file = tmp_path / "test.txt"
        test_content = b"test content"
        test_file.write_bytes(test_content)

        expected_md5 = "9473fdd0d880a43c21b7778d34872157"
        result = calculator.calculate_md5(test_file)
        assert result == expected_md5

    def test_calculate_md5_empty_file(self, calculator, tmp_path):
        """Test MD5 calculation with an empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_bytes(b"")

        expected_md5 = "d41d8cd98f00b204e9800998ecf8427e"  # MD5 of empty file
        result = calculator.calculate_md5(test_file)
        assert result == expected_md5

    def test_calculate_md5_large_file(self, calculator, tmp_path):
        """Test MD5 calculation with a large file (tests chunking)."""
        test_file = tmp_path / "large.txt"
        test_content = b"x" * 8192  # Create content larger than chunk size
        test_file.write_bytes(test_content)
        
        result = calculator.calculate_md5(test_file)
        assert len(result) == 32  # Valid MD5 hash length
        assert result.isalnum()  # Contains only hexadecimal characters

    def test_calculate_md5_nonexistent_file(self, calculator):
        """Test MD5 calculation with a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            calculator.calculate_md5(Path("nonexistent.txt"))

    def test_get_file_size_valid_file(self, calculator, tmp_path):
        """Test file size calculation with a valid file."""
        test_file = tmp_path / "test.txt"
        test_content = b"test content"
        test_file.write_bytes(test_content)

        expected_size = len(test_content)
        result = calculator.get_file_size(test_file)
        assert result == expected_size

    def test_get_file_size_empty_file(self, calculator, tmp_path):
        """Test file size calculation with an empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_bytes(b"")

        result = calculator.get_file_size(test_file)
        assert result == 0

    def test_get_file_size_nonexistent_file(self, calculator):
        """Test file size calculation with a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            calculator.get_file_size(Path("nonexistent.txt"))
