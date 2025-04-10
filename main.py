from pathlib import Path

from create_metadata_per_sequence import generate_metadata
from create_table import create_table

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent
SEQUENCES_DIR = PROJECT_ROOT / 'sequences'
METADATA_DIR = PROJECT_ROOT / 'metadata'

if __name__ == '__main__':
    for file_path in list(SEQUENCES_DIR.glob('*.json')):
        generate_metadata(file_path, output_dir_path=METADATA_DIR)

    create_table()