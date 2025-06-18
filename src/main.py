"""
Main script for CTDC data curation workflow.
"""
from pathlib import Path
import logging
from file_management.file_renamer import FileRenamer
from manifest.manifest_generator import ManifestGenerator
from utils.file_utils import ensure_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the data curation workflow."""
    # Define paths
    base_path = Path(__file__).parent.parent
    input_dir = base_path / "data" / "input"
    output_dir = base_path / "data" / "output"
    manifest_path = output_dir / "transfer_manifest.csv"

    # Ensure output directory exists
    ensure_directory(output_dir)

    try:
        # Initialize components
        renamer = FileRenamer()
        manifest_gen = ManifestGenerator()

        # Generate manifest
        logger.info("Generating transfer manifest...")
        manifest = manifest_gen.generate_manifest(input_dir, manifest_path)
        logger.info(f"Manifest generated successfully at: {manifest_path}")
        logger.info(f"Total files processed: {len(manifest)}")

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()
