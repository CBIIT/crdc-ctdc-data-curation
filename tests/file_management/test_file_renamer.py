"""
Unit tests for the FileRenamer class.
"""
import pytest
from pathlib import Path
from src.file_management.file_renamer import FileRenamer

@pytest.fixture
def renamer():
    """Fixture providing a FileRenamer instance."""
    return FileRenamer()

@pytest.fixture
def sample_paths():
    """Fixture providing sample file paths for testing."""
    return {
        'vcf': Path('MSB-00123-01_variant_calls.vcf'),
        'pdf': Path('MSB-00123-01_genomic_report.pdf'),
        'invalid': Path('invalid_filename.vcf')
    }

class TestFileRenamer:
    """Tests for the FileRenamer class."""

    @pytest.mark.parametrize("filename,expected", [
        ("MSB-00123-01_variant_calls.vcf", "MSB-00123-01-somatic-mutations-CTDCv1.vcf"),
        ("MSB-12345-02_variant_calls.vcf", "MSB-12345-02-somatic-mutations-CTDCv1.vcf"),
    ])
    def test_rename_vcf_file_valid_input(self, renamer, filename, expected):
        """Test renaming a VCF file with valid input."""
        result = renamer.rename_vcf_file(Path(filename))
        assert result == expected

    def test_rename_pdf_file_valid_input(self, renamer, sample_paths):
        """Test renaming a PDF file with valid input."""
        expected = "MSB-00123-01-genomic-report-CTDCv1.pdf"
        result = renamer.rename_pdf_file(sample_paths['pdf'])
        assert result == expected

    def test_rename_vcf_file_invalid_input(self, renamer, sample_paths):
        """Test renaming a VCF file with invalid input raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            renamer.rename_vcf_file(sample_paths['invalid'])
        assert "Invalid filename format" in str(exc_info.value)

    def test_rename_pdf_file_invalid_input(self, renamer, sample_paths):
        """Test renaming a PDF file with invalid input raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            renamer.rename_pdf_file(sample_paths['invalid'])
        assert "Invalid filename format" in str(exc_info.value)

    @pytest.mark.parametrize("filename,expected", [
        ('MSB-00123-01_test.vcf', True),
        ('MSB-12345-02_test.vcf', True),
        ('invalid_file.vcf', False),
        ('MSB-1234-01_test.vcf', False),  # Too few digits
        ('MSB-123456-01_test.vcf', False),  # Too many digits
    ])
    def test_validate_filename(self, renamer, filename, expected):
        """Test filename validation with various inputs."""
        assert renamer._validate_filename(filename) == expected

    @pytest.mark.parametrize("filename,expected", [
        ('MSB-00123-01_test.vcf', 'MSB-00123-01'),
        ('MSB-12345-02_test.pdf', 'MSB-12345-02'),
    ])
    def test_extract_specimen_id_valid(self, renamer, filename, expected):
        """Test specimen ID extraction with valid inputs."""
        assert renamer._extract_specimen_id(filename) == expected

    def test_extract_specimen_id_invalid(self, renamer):
        """Test specimen ID extraction with invalid input raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            renamer._extract_specimen_id('invalid_file.vcf')
        assert "Could not extract valid specimen ID" in str(exc_info.value)
