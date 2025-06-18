"""
Unit tests for the MetadataExtractor class.
"""
import pytest
from pathlib import Path
from src.manifest.metadata_extractor import MetadataExtractor

@pytest.fixture
def extractor():
    """Fixture providing a MetadataExtractor instance."""
    return MetadataExtractor()

class TestMetadataExtractor:
    """Tests for the MetadataExtractor class."""

    @pytest.mark.parametrize("filename,expected", [
        ("MSB-00123-01_test.vcf", "MSB-00123-01"),
        ("MSB-12345-02_genomic.pdf", "MSB-12345-02"),
    ])
    def test_extract_specimen_id_valid(self, extractor, filename, expected):
        """Test specimen ID extraction with valid inputs."""
        result = extractor.extract_specimen_id(filename)
        assert result == expected

    @pytest.mark.parametrize("invalid_filename", [
        "invalid.vcf",
        "MSB-1234-01.vcf",  # Too few digits
        "MSB-123456-01.vcf",  # Too many digits
        "ABC-12345-01.vcf",  # Wrong prefix
    ])
    def test_extract_specimen_id_invalid(self, extractor, invalid_filename):
        """Test specimen ID extraction with invalid inputs raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor.extract_specimen_id(invalid_filename)
        assert "Invalid specimen ID format" in str(exc_info.value)

    @pytest.mark.parametrize("filename,expected", [
        ("MSB-00123_test.vcf", "MSB-00123"),
        ("MSB-12345_genomic.pdf", "MSB-12345"),
    ])
    def test_extract_subject_id_valid(self, extractor, filename, expected):
        """Test subject ID extraction with valid inputs."""
        result = extractor.extract_subject_id(filename)
        assert result == expected

    @pytest.mark.parametrize("invalid_filename", [
        "invalid.vcf",
        "MSB-1234.vcf",  # Too few digits
        "MSB-123456.vcf",  # Too many digits
        "ABC-12345.vcf",  # Wrong prefix
    ])
    def test_extract_subject_id_invalid(self, extractor, invalid_filename):
        """Test subject ID extraction with invalid inputs raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor.extract_subject_id(invalid_filename)
        assert "Invalid subject ID format" in str(exc_info.value)

    def test_get_file_metadata_clinical_report(self, extractor):
        """Test metadata extraction for clinical report files."""
        filename = "MSB-12345-01_clinical-report.pdf"
        file_path = Path(filename)
        
        expected_metadata = {
            'data_file_name': filename,
            'subject.subject_id': 'MSB-12345'
        }
        
        result = extractor.get_file_metadata(file_path)
        assert result == expected_metadata

    def test_get_file_metadata_genomic_file(self, extractor):
        """Test metadata extraction for genomic files."""
        filename = "MSB-12345-01_genomic.vcf"
        file_path = Path(filename)
        
        expected_metadata = {
            'data_file_name': filename,
            'specimen.specimen_id': 'MSB-12345-01'
        }
        
        result = extractor.get_file_metadata(file_path)
        assert result == expected_metadata
