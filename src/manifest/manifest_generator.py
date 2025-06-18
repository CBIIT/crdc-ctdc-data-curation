"""
Module for generating file transfer manifests.
"""
from pathlib import Path
from typing import List, Dict
import pandas as pd
from src.file_management.checksum import ChecksumCalculator
from src.manifest.metadata_extractor import MetadataExtractor

class ManifestGenerator:
    """Class for generating file transfer manifests with required metadata."""

    def __init__(self):
        """Initialize ManifestGenerator with required dependencies."""
        self.metadata_extractor = MetadataExtractor()
        self.checksum_calculator = ChecksumCalculator()

    def generate_manifest(self, input_dir: Path, output_path: Path) -> pd.DataFrame:
        """
        Creates transfer manifest for all files with required metadata fields.

        Args:
            input_dir (Path): Directory containing the files
            output_path (Path): Path where manifest will be saved

        Returns:
            pd.DataFrame: Generated manifest

        Raises:
            FileNotFoundError: If input directory doesn't exist
            IOError: If manifest cannot be written
        """
        all_data = []
        
        # Process each file type
        vcf_files = list(input_dir.glob("**/*somatic-mutations*.vcf"))
        genomic_files = list(input_dir.glob("**/*genomic-report*.pdf"))
        clinical_files = list(input_dir.glob("**/*clinical-report*.pdf"))

        all_data.extend(self._process_somatic_mutations(vcf_files))
        all_data.extend(self._process_genomic_reports(genomic_files))
        all_data.extend(self._process_clinical_reports(clinical_files))

        # Create DataFrame and save
        df = pd.DataFrame(all_data)
        df.to_csv(output_path, index=False)
        return df

    def _process_somatic_mutations(self, files: List[Path]) -> List[Dict]:
        """Process somatic mutation VCF files."""
        results = []
        for file_path in files:
            metadata = self.metadata_extractor.get_file_metadata(file_path)
            metadata.update({
                'type': 'data_file',
                'data_file_type': 'Variant Call File',
                'data_file_description': 'Unfiltered Oncomine variant analysis',
                'data_file_checksum_type': 'md5sum',
                'data_file_compression_status': 'Uncompressed',
                'data_file_size': self.checksum_calculator.get_file_size(file_path),
                'data_file_checksum_value': self.checksum_calculator.calculate_md5(file_path)
            })
            results.append(metadata)
        return results

    def _process_genomic_reports(self, files: List[Path]) -> List[Dict]:
        """Process genomic report PDF files."""
        results = []
        for file_path in files:
            metadata = self.metadata_extractor.get_file_metadata(file_path)
            metadata.update({
                'type': 'data_file',
                'data_file_type': 'Variant Report',
                'data_file_description': 'Validated Oncomine-derived variant analysis',
                'data_file_checksum_type': 'md5sum',
                'data_file_compression_status': 'Uncompressed',
                'data_file_size': self.checksum_calculator.get_file_size(file_path),
                'data_file_checksum_value': self.checksum_calculator.calculate_md5(file_path)
            })
            results.append(metadata)
        return results

    def _process_clinical_reports(self, files: List[Path]) -> List[Dict]:
        """Process clinical report PDF files."""
        results = []
        for file_path in files:
            metadata = self.metadata_extractor.get_file_metadata(file_path)
            metadata.update({
                'type': 'data_file',
                'data_file_type': 'Clinical Report',
                'data_file_description': 'Detailed clinical evaluation',
                'data_file_checksum_type': 'md5sum',
                'data_file_compression_status': 'Uncompressed',
                'data_file_size': self.checksum_calculator.get_file_size(file_path),
                'data_file_checksum_value': self.checksum_calculator.calculate_md5(file_path)
            })
            results.append(metadata)
        return results
