import pandas as pd
import json
from pathlib import Path


# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent
METADATA_DIR = PROJECT_ROOT / 'metadata'
OUTPUT_CSV = PROJECT_ROOT / 'metadata.csv'
sequence_id = 'sequence_id'


def create_table():
    l = []
    print(f"Looking for *.metadata.json files in: {METADATA_DIR}")
    for file_path in list(METADATA_DIR.glob('*.metadata.json')):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data[sequence_id] = file_path.stem.replace('.metadata', '')
        l.append(data)
    print(f"\nCreating DataFrame and writing to CSV...")
    df = pd.DataFrame(l)
    df.insert(0, sequence_id, df.pop(sequence_id))  # move primary key to leftmost column
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"\nSuccessfully created '{OUTPUT_CSV}' with data from {len(l)} file(s).")


if __name__ == '__main__':

    create_table()
