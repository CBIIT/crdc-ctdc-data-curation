"""
Shared test fixtures and configuration.
"""
import pytest
from pathlib import Path

@pytest.fixture
def test_data_dir(tmp_path):
    """Create and return a temporary directory with test data files."""
    # Create test VCF files
    vcf_dir = tmp_path / "VCF_Report"
    vcf_dir.mkdir()
    (vcf_dir / "MSB-00123-01_variant_calls.vcf").touch()
    (vcf_dir / "MSB-00124-02_variant_calls.vcf").touch()

    # Create test PDF reports
    pdf_dir = tmp_path / "Biomarker_Report"
    pdf_dir.mkdir()
    (pdf_dir / "MSB-00123-01_genomic_report.pdf").touch()
    (pdf_dir / "MSB-00124-02_clinical_report.pdf").touch()

    return tmp_path
