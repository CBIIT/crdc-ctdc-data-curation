"""
Main script for CTDC data curation workflow.
"""
from pathlib import Path
import logging
import sys
from typing import Optional
import click
from src.file_management.file_renamer import FileRenamer
from src.manifest.manifest_generator import ManifestGenerator
from src.utils.file_utils import ensure_directory
from src.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)

@click.group()
@click.option(
    '--log-level',
    default='INFO',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
    help='Set the logging level'
)
@click.option(
    '--log-file',
    type=click.Path(),
    help='Optional log file path'
)
def cli(log_level: str, log_file: Optional[str]) -> None:
    """Data curation tools for CMB files."""
    try:
        configure_logging(
            log_level=log_level,
            log_file=Path(log_file) if log_file else None
        )
    except Exception as e:
        print(f"Failed to configure logging: {e}", file=sys.stderr)
        sys.exit(1)

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output_dir', type=click.Path(file_okay=False))
@click.option(
    '--dry-run',
    is_flag=True,
    help='Show what would be renamed without making changes'
)
def rename_files(input_dir: str, output_dir: str, dry_run: bool) -> None:
    """Rename files according to CTDC conventions and save to output directory.
    
    Args:
        input_dir: Directory containing files to rename
        output_dir: Directory where renamed files will be saved
        dry_run: If True, show what would be renamed without making changes
    """
    try:
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        renamer = FileRenamer()

        # Ensure output directory exists
        if not dry_run:
            ensure_directory(output_path)

        logger.info(f"{'Dry run: ' if dry_run else ''}Processing files in {input_path}")
        logger.info(f"{'Dry run: ' if dry_run else ''}Output directory: {output_path}")

        # Process all supported files (VCF and PDF)
        for extension in ['.vcf', '.pdf']:
            for file in input_path.glob(f"**/*{extension}"):
                try:
                    new_name, new_path = renamer.rename_and_copy(file, output_path, dry_run)
                    if dry_run:
                        logger.info(f"Would rename {file.name} to {new_name}")
                    else:
                        logger.info(f"Renamed and copied {file.name} to {new_path}")
                except ValueError as e:
                    logger.error(f"Error processing {file}: {e}")
                
    except Exception as e:
        logger.error(f"Failed to process directory {input_dir}: {e}")
        sys.exit(1)

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output_file', type=click.Path(file_okay=True, dir_okay=False))
def generate_manifest(input_dir: str, output_file: str) -> None:
    """Generate transfer manifest for files."""
    try:
        input_path = Path(input_dir)
        output_path = Path(output_file)
        
        # Ensure output directory exists
        ensure_directory(output_path.parent)
        
        generator = ManifestGenerator()
        manifest = generator.generate_manifest(input_path, output_path)
        logger.info(f"Generated manifest with {len(manifest)} entries")
        
    except Exception as e:
        logger.error(f"Failed to generate manifest: {e}")
        sys.exit(1)

def main():
    """Main function to run the data curation workflow."""
    # Default behavior when run without CLI arguments
    base_path = Path(__file__).parent.parent
    input_dir = base_path / "data" / "input"
    output_dir = base_path / "data" / "output"
    manifest_path = output_dir / "transfer_manifest.csv"

    # Ensure output directory exists
    ensure_directory(output_dir)

    try:
        # Initialize components
        manifest_gen = ManifestGenerator()

        # Generate manifest
        logger.info("Generating transfer manifest...")
        manifest = manifest_gen.generate_manifest(input_dir, manifest_path)
        logger.info(f"Manifest generated successfully at: {manifest_path}")
        logger.info(f"Total files processed: {len(manifest)}")

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    cli()
