"""
Restore from Word Document for Power BI Projects

Parses a flattened Word document and restores the original file structure.
This completes the round-trip workflow: flatten -> edit -> restore.
"""

import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from docx import Document


# Load environment variables
load_dotenv()

# File delimiter markers (must match directory_flattener.py)
FILE_START_PATTERN = r"═══ FILE: (.+?) ═══"
FILE_END_MARKER = "═══ END FILE ═══"


def extract_files_from_word(word_file: str) -> dict[str, str]:
    """
    Extract file contents from a flattened Word document.

    Args:
        word_file: Path to the Word document

    Returns:
        Dictionary mapping relative file paths to their content
    """
    doc = Document(word_file)

    files = {}
    current_file = None
    current_content = []
    in_file_block = False

    for para in doc.paragraphs:
        text = para.text.strip()

        # Check for file start marker (in headings)
        start_match = re.match(FILE_START_PATTERN, text)
        if start_match:
            # If we were already in a file block, save it first
            if current_file and current_content:
                files[current_file] = '\n'.join(current_content)

            # Start new file block
            current_file = start_match.group(1)
            current_content = []
            in_file_block = True
            continue

        # Check for file end marker
        if text == FILE_END_MARKER:
            if current_file and current_content:
                files[current_file] = '\n'.join(current_content)
            current_file = None
            current_content = []
            in_file_block = False
            continue

        # If we're in a file block, collect content
        if in_file_block and current_file:
            # Use original paragraph text (preserve whitespace)
            current_content.append(para.text)

    # Handle case where last file didn't have end marker
    if current_file and current_content:
        files[current_file] = '\n'.join(current_content)

    return files


def validate_json(content: str, file_path: str) -> tuple[bool, str | None]:
    """
    Validate JSON content.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path.endswith('.json'):
        return True, None

    try:
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSON error at line {e.lineno}, col {e.colno}: {e.msg}"


def restore_files(files: dict[str, str], output_dir: str) -> tuple[int, int, list[str]]:
    """
    Write extracted files to the output directory.

    Args:
        files: Dictionary mapping relative paths to content
        output_dir: Base directory to write files to

    Returns:
        Tuple of (files_written, files_failed, error_messages)
    """
    output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    files_written = 0
    files_failed = 0
    errors = []

    for relative_path, content in files.items():
        file_path = output_path / relative_path

        # Validate JSON files before writing
        is_valid, error_msg = validate_json(content, relative_path)
        if not is_valid:
            print(f"  [INVALID JSON] {relative_path}")
            print(f"    {error_msg}")
            errors.append(f"{relative_path}: {error_msg}")
            files_failed += 1
            continue

        try:
            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  [OK] {relative_path}")
            files_written += 1

        except Exception as e:
            print(f"  [ERROR] {relative_path}: {e}")
            errors.append(f"{relative_path}: {e}")
            files_failed += 1

    return files_written, files_failed, errors


def restore_from_word(word_file: str, output_dir: str) -> None:
    """
    Restore a .Report folder from a flattened Word document.

    Args:
        word_file: Path to the edited Word document
        output_dir: Path to output .Report folder
    """
    word_path = Path(word_file)

    if not word_path.exists():
        raise FileNotFoundError(f"Word document not found: {word_file}")

    print(f"Parsing Word document...")
    files = extract_files_from_word(word_file)

    if not files:
        raise ValueError("No files found in Word document. Check that FILE markers are intact.")

    print(f"Found {len(files)} files to restore.\n")
    print("Restoring files:")

    files_written, files_failed, errors = restore_files(files, output_dir)

    print(f"\n{'='*50}")
    print(f"Restoration complete!")
    print(f"  Files written: {files_written}")
    print(f"  Files failed:  {files_failed}")
    print(f"  Output: {Path(output_dir).absolute()}")

    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nPlease fix the errors above and run again.")


def main():
    """Main entry point."""
    input_word = os.getenv('INPUT_WORD_DOC')
    output_dir = os.getenv('OUTPUT_REPORT_DIR')

    if not input_word:
        raise ValueError("INPUT_WORD_DOC not set in .env file")
    if not output_dir:
        raise ValueError("OUTPUT_REPORT_DIR not set in .env file")

    print(f"Restore from Word")
    print(f"{'='*50}")
    print(f"Input:  {input_word}")
    print(f"Output: {output_dir}")
    print(f"{'='*50}\n")

    restore_from_word(input_word, output_dir)


if __name__ == '__main__':
    main()
