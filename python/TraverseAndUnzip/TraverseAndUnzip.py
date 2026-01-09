# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2026/1/9 18:20
# @File    : TraverseAndUnzip.py
# @Project : myscripts
# @Author  : kshi
# @Desc    : Traverse a directory and unzip all zipped files
# @Copyright : © 2026 . All rights reserved.
# @Version : 1.0.0
# --------------------------------------
import zipfile
import os
import sys
import argparse
from pathlib import Path


def find_zip_files(directory):
    """
    Recursively find all zip files in the given directory.

    Args:
        directory: Root directory to search

    Returns:
        List of Path objects for all zip files found
    """
    zip_files = []
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return zip_files

    if not dir_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return zip_files

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                zip_files.append(Path(root) / file)

    return zip_files


def generate_file_tree(zip_files, base_dir):
    """
    Generate a file tree representation of zip files.

    Args:
        zip_files: List of Path objects for zip files
        base_dir: Base directory for relative paths

    Returns:
        String representation of the file tree
    """
    if not zip_files:
        return "No zip files found."

    base_path = Path(base_dir)
    tree_lines = ["# Zip Files Found", ""]

    # Create a tree structure
    tree_dict = {}
    for zip_file in zip_files:
        rel_path = zip_file.relative_to(base_path)
        parts = rel_path.parts

        current = tree_dict
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = None  # It's a file
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]

    # Convert tree dict to string
    def dict_to_tree(d, indent=0):
        lines = []
        items = sorted(d.items())
        for name, value in items:
            prefix = "  " * indent + ("└── " if indent > 0 else "")
            if value is None:
                lines.append(prefix + name)
            else:
                lines.append(prefix + name + "/")
                lines.extend(dict_to_tree(value, indent + 1))
        return lines

    tree_lines.extend(dict_to_tree(tree_dict))
    return "\n".join(tree_lines)


def save_initial_report(zip_files, base_dir):
    """
    Save the initial file tree report to {dir}/report/{dirname}.md

    Args:
        zip_files: List of Path objects for zip files
        base_dir: Base directory path

    Returns:
        Path to the report file
    """
    base_path = Path(base_dir)
    report_dir = base_path / "report"
    report_dir.mkdir(exist_ok=True, parents=True)

    dir_name = base_path.name
    report_file = report_dir / f"{dir_name}.md"

    file_tree = generate_file_tree(zip_files, base_dir)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(file_tree)

    return report_file


def unzip_file(zip_path):
    """
    Unzip a file into a new directory with the same name as the zip file.

    Args:
        zip_path: Path to the zip file

    Returns:
        List of extracted file paths
    """
    extracted_files = []

    # Create directory name from zip file name (without .zip extension)
    dir_name = zip_path.stem
    extract_dir = zip_path.parent / dir_name

    try:
        # Create extraction directory if it doesn't exist
        extract_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            zip_ref.extractall(extract_dir)
            extracted_files = [extract_dir / file for file in file_list]
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")

    return extracted_files


def generate_final_report(zip_files, extraction_results, base_dir):
    """
    Generate a final report showing zipped and unzipped files.

    Args:
        zip_files: List of Path objects for zip files
        extraction_results: Dictionary mapping zip files to their extracted contents
        base_dir: Base directory path

    Returns:
        String representation of the final report
    """
    report_lines = [
        "# Unzip Operation Report",
        f"",
        f"**Base Directory:** {base_dir}",
        f"**Total Zip Files Found:** {len(zip_files)}",
        f"",
        "## Files Extracted",
        f""
    ]

    if not zip_files:
        report_lines.append("No zip files found to extract.")
        return "\n".join(report_lines)

    for zip_file in zip_files:
        rel_path = zip_file.relative_to(base_dir)
        report_lines.append(f"### 📦 {rel_path}")
        report_lines.append(f"**Location:** `{zip_file.parent}`")

        extracted = extraction_results.get(zip_file, [])
        if extracted:
            report_lines.append(f"**Extracted {len(extracted)} file(s):**")
            for file in extracted:
                report_lines.append(f"  - `{file.name}`")
        else:
            report_lines.append("**Status:** Failed to extract or empty archive")
        report_lines.append("")

    return "\n".join(report_lines)


def save_final_report(report_content, base_dir):
    """
    Save the final report to {dir}/report/{dirname}_final.md

    Args:
        report_content: Content of the final report
        base_dir: Base directory path

    Returns:
        Path to the final report file
    """
    base_path = Path(base_dir)
    report_dir = base_path / "report"
    report_dir.mkdir(exist_ok=True, parents=True)

    dir_name = base_path.name
    report_file = report_dir / f"{dir_name}_final.md"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return report_file


def delete_zip_files(zip_files):
    """
    Delete zip files after successful extraction.

    Args:
        zip_files: List of Path objects for zip files to delete

    Returns:
        Tuple of (successful_deletions, failed_deletions)
    """
    successful = []
    failed = []

    for zip_file in zip_files:
        try:
            zip_file.unlink()
            successful.append(zip_file)
        except Exception as e:
            print(f"Error deleting {zip_file}: {e}")
            failed.append(zip_file)

    return successful, failed


def get_all_files(directory):
    """
    Get all files in the directory recursively.

    Args:
        directory: Root directory to search

    Returns:
        List of Path objects for all files found
    """
    all_files = []
    dir_path = Path(directory)

    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(Path(root) / file)

    return sorted(all_files)


def generate_complete_file_tree(files, base_dir):
    """
    Generate a complete file tree representation of all files.

    Args:
        files: List of Path objects for all files
        base_dir: Base directory for relative paths

    Returns:
        String representation of the file tree
    """
    if not files:
        return "No files found."

    base_path = Path(base_dir)
    tree_lines = ["# Complete File Tree (After Unzip)", ""]

    # Create a tree structure
    tree_dict = {}
    for file in files:
        try:
            rel_path = file.relative_to(base_path)
            parts = rel_path.parts

            current = tree_dict
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = None  # It's a file
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        except ValueError:
            # Skip files that are not relative to base path
            continue

    # Convert tree dict to string
    def dict_to_tree(d, indent=0):
        lines = []
        items = sorted(d.items())
        for name, value in items:
            prefix = "  " * indent + ("└── " if indent > 0 else "")
            if value is None:
                lines.append(prefix + name)
            else:
                lines.append(prefix + name + "/")
                lines.extend(dict_to_tree(value, indent + 1))
        return lines

    tree_lines.extend(dict_to_tree(tree_dict))

    # Add summary
    tree_lines.append("")
    tree_lines.append(f"**Total Files:** {len(files)}")

    return "\n".join(tree_lines)


def save_unzipped_report(base_dir):
    """
    Save the complete file tree after unzipping to {dir}/report/{dirname}_unzipped.md

    Args:
        base_dir: Base directory path

    Returns:
        Path to the unzipped report file
    """
    base_path = Path(base_dir)
    report_dir = base_path / "report"
    report_dir.mkdir(exist_ok=True, parents=True)

    dir_name = base_path.name
    report_file = report_dir / f"{dir_name}_unzipped.md"

    all_files = get_all_files(base_dir)
    file_tree = generate_complete_file_tree(all_files, base_dir)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(file_tree)

    return report_file


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Namespace object containing parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Traverse a directory and unzip all zipped files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python TraverseAndUnzip.py /path/to/directory
  python TraverseAndUnzip.py .                    # Current directory
  python TraverseAndUnzip.py ~/Documents/archives
        """
    )

    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory path to traverse (default: current directory)'
    )

    return parser.parse_args()


def main():
    """
    Main function to orchestrate the traverse and unzip operation.
    """
    args = parse_arguments()

    print("=== Traverse and Unzip Utility ===")
    print("")

    # Step 1: Get directory from command-line argument
    directory = args.directory

    print(f"\nTraversing directory: {directory}")
    print("-" * 50)

    # Step 2: Traverse the directory and find all zip files
    all_zip_files = find_zip_files(directory)

    if not all_zip_files:
        print("No zip files found in the specified directory.")
        return

    print(f"Found {len(all_zip_files)} zip file(s):")
    for zip_file in all_zip_files:
        print(f"  - {zip_file}")

    print("-" * 50)

    # Step 3: Save file tree to {dir}/report/{dir}.md
    print("\nGenerating initial file tree report...")
    initial_report = save_initial_report(all_zip_files, directory)
    print(f"Initial report saved to: {initial_report}")

    # Step 4 & 5: Recursively unzip until no more zip files exist
    print("\nExtracting zip files (checking for nested zips)...")
    extraction_results = {}
    round_number = 1
    original_zip_files = set(all_zip_files)

    while True:
        print(f"\n--- Round {round_number} ---")

        # Find current zip files
        current_zips = find_zip_files(directory)

        if not current_zips:
            print("No more zip files found. Extraction complete!")
            break

        # Filter out already processed zips (in first round, all are new)
        new_zips = [z for z in current_zips if z not in extraction_results]

        if not new_zips:
            print("All remaining zip files already processed. Extraction complete!")
            break

        print(f"Found {len(new_zips)} new zip file(s) to extract:")

        # Extract all new zip files
        for i, zip_file in enumerate(new_zips, 1):
            print(f"  [{i}/{len(new_zips)}] Extracting: {zip_file.relative_to(directory)}")
            extracted = unzip_file(zip_file)
            extraction_results[zip_file] = extracted
            if extracted:
                print(f"    ✓ Extracted {len(extracted)} file(s)")

        round_number += 1

    print("-" * 50)

    # Step 5 (continued): Generate and save final report
    print("\nGenerating final report...")
    final_report_content = generate_final_report(
        list(extraction_results.keys()),
        extraction_results,
        directory
    )
    final_report = save_final_report(final_report_content, directory)
    print(f"Final report saved to: {final_report}")

    # Step 6: Delete ALL processed zip files (including nested ones)
    print("\nDeleting all processed zip files...")
    all_processed_zips = list(extraction_results.keys())
    successful_deletions, failed_deletions = delete_zip_files(all_processed_zips)
    print(f"Successfully deleted: {len(successful_deletions)} file(s)")
    if failed_deletions:
        print(f"Failed to delete: {len(failed_deletions)} file(s)")
        for failed in failed_deletions:
            print(f"  - {failed}")

    # Step 7: List all files and save complete file tree
    print("\nGenerating complete file tree after unzip...")
    unzipped_report = save_unzipped_report(directory)
    print(f"Complete file tree saved to: {unzipped_report}")

    print("")
    print("=== Operation Complete ===")
    print(f"Total zip files processed: {len(extraction_results)}")
    print(f"Rounds of extraction: {round_number - 1}")
    print(f"Reports saved in: {Path(directory) / 'report'}")


if __name__ == "__main__":
    main()