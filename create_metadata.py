import json
import statistics
from pathlib import Path
import argparse
import sys


def calculate_inversions(sequence):
    """Calculates the number of inversions (pairs i<j where seq[i]>seq[j]). O(n^2)."""
    n = len(sequence)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if sequence[i] > sequence[j]:
                count += 1
    return count



def generate_metadata(sequence_file_path: Path, output_dir_path: Path):
    """Generates and saves metadata for a given sequence file."""

    print(f"\nProcessing sequence file: {sequence_file_path.name}")

    # 1. Validate input file path
    if not sequence_file_path.is_file():
        print(f"  Error: Input sequence file not found: {sequence_file_path}")
        return False

    # 2. Read sequence data
    try:
        with open(sequence_file_path, 'r', encoding='utf-8') as f:
            sequence = json.load(f)
        if not isinstance(sequence, list):
            print(f"Error: Input file does not contain a valid JSON list: {sequence_file_path}")
            return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {sequence_file_path}")
        return False
    except IOError as e:
        print(f"Error: Cannot read input file: {sequence_file_path} - {e}")
        return False

    # 3. Basic checks and type determination
    n = len(sequence)
    if n == 0:
        print("Warning: Sequence is empty. Some metadata fields will be null.")

    # 4. Calculate metadata fields
    metadata = {}
    distinct_element_count = len(set(sequence))

    metadata['length'] = n
    metadata['is_sorted'] = sequence == sorted(sequence)
    metadata['is_reverse_sorted'] = sequence == sorted(sequence, reverse=True)
    metadata['inversion_count'] = calculate_inversions(sequence)
    metadata['min_value'] = min(sequence)
    metadata['max_value'] = max(sequence)
    metadata['range'] = max(sequence) - min(sequence)
    metadata['contains_duplicates'] = n != distinct_element_count
    metadata['duplicate_count'] = n - distinct_element_count
    metadata['distinct_element_count'] = distinct_element_count
    metadata['mean'] = statistics.mean(sequence)
    metadata['median'] = statistics.median(sequence)
    metadata['variance'] = statistics.variance(sequence)
    metadata['standard_deviation'] = round(statistics.stdev(sequence), 3)

    output_filename = sequence_file_path.stem + ".metadata.json"
    output_file_path = output_dir_path / output_filename

    # Ensure output directory exists
    try:
        output_dir_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"  Error: Could not create output directory: {output_dir_path} - {e}")
        return False

    # 6. Write JSON output
    print(f"Writing metadata to: {output_file_path}")
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"  Error: Could not write metadata file: {output_file_path} - {e}")
        return False
    except TypeError as e:
        print(f"  Error: Could not serialize metadata to JSON (check data types, e.g. mode): {e}")
        return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a detailed metadata JSON file for a sequence JSON file."
    )
    parser.add_argument(
        "sequence_file",
        type=Path,
        help="Path to the input sequence file (e.g., sequences/run5.json)",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("metadata"), # Default to 'metadata' subdir in current dir
        help="Directory to save the output metadata file (default: ./metadata/)",
    )

    args = parser.parse_args()

    success = generate_metadata(
        sequence_file_path=args.sequence_file.resolve(),
        output_dir_path=args.output_dir.resolve()
    )

    if success:
        print("\nMetadata generation completed successfully.")
        sys.exit(0)
    else:
        print("\nMetadata generation failed.")
        sys.exit(1)