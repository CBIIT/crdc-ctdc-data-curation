"""
Unit tests for the ManifestGenerator class.
"""
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch
from src.manifest.manifest_generator import ManifestGenerator

@pytest.fixture
def mock_metadata_extractor():
    """Fixture providing a mocked MetadataExtractor."""
    mock = Mock()
    mock.get_file_metadata.return_value = {
        'data_file_name': 'test.vcf',
        'specimen.specimen_id': 'MSB-00123-01'
    }
    return mock

@pytest.fixture
def mock_checksum_calculator():
    """Fixture providing a mocked ChecksumCalculator."""
    mock = Mock()
    mock.calculate_md5.return_value = "testmd5hash"
    mock.get_file_size.return_value = 1000
    return mock

@pytest.fixture
def generator(mock_metadata_extractor, mock_checksum_calculator):
    """Fixture providing a ManifestGenerator with mocked dependencies."""
    gen = ManifestGenerator()
    gen.metadata_extractor = mock_metadata_extractor
    gen.checksum_calculator = mock_checksum_calculator
    return gen

class TestManifestGenerator:
    """Tests for the ManifestGenerator class."""

    def test_generate_manifest_empty_directory(self, generator, tmp_path):
        """Test manifest generation with empty directory."""
        manifest_path = tmp_path / "manifest.csv"
        result = generator.generate_manifest(tmp_path, manifest_path)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_generate_manifest_with_vcf_files(self, generator, tmp_path):
        """Test manifest generation with VCF files."""
        # Create test VCF file
        vcf_file = tmp_path / "MSB-00123-01_somatic-mutations.vcf"
        vcf_file.touch()

        manifest_path = tmp_path / "manifest.csv"
        result = generator.generate_manifest(tmp_path, manifest_path)

        assert len(result) == 1
        assert result.iloc[0]['type'] == 'data_file'
        assert result.iloc[0]['data_file_type'] == 'Variant Call File'
        assert result.iloc[0]['data_file_checksum_type'] == 'md5sum'

    def test_generate_manifest_with_genomic_reports(self, generator, tmp_path):
        """Test manifest generation with genomic report files."""
        # Create test genomic report file
        report_file = tmp_path / "MSB-00123-01_genomic-report.pdf"
        report_file.touch()

        manifest_path = tmp_path / "manifest.csv"
        result = generator.generate_manifest(tmp_path, manifest_path)

        assert len(result) == 1
        assert result.iloc[0]['type'] == 'data_file'
        assert result.iloc[0]['data_file_type'] == 'Variant Report'

    def test_generate_manifest_missing_directory(self, generator):
        """Test manifest generation with nonexistent directory raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            generator.generate_manifest(Path("/nonexistent"), Path("manifest.csv"))

    @patch('pathlib.Path.glob')
    def test_process_somatic_mutations(self, mock_glob, generator, tmp_path):
        """Test processing of somatic mutation VCF files."""
        test_file = tmp_path / "test.vcf"
        mock_glob.return_value = [test_file]
        
        results = generator._process_somatic_mutations([test_file])
        assert len(results) == 1
        
        metadata = results[0]
        assert metadata['type'] == 'data_file'
        assert metadata['data_file_type'] == 'Variant Call File'
        assert metadata['data_file_checksum_value'] == "testmd5hash"
        assert metadata['data_file_size'] == 1000

    @patch('pathlib.Path.glob')
    def test_process_genomic_reports(self, mock_glob, generator, tmp_path):
        """Test processing of genomic report files."""
        test_file = tmp_path / "test.pdf"
        mock_glob.return_value = [test_file]
        
        results = generator._process_genomic_reports([test_file])
        assert len(results) == 1
        
        metadata = results[0]
        assert metadata['type'] == 'data_file'
        assert metadata['data_file_type'] == 'Variant Report'
        assert metadata['data_file_checksum_value'] == "testmd5hash"
        assert metadata['data_file_size'] == 1000
