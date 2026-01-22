"""Script to remove all emojis from the project."""

import re
from pathlib import Path

# Comprehensive emoji regex pattern
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)

def remove_emojis_from_text(text):
    """Remove emojis from text."""
    return EMOJI_PATTERN.sub('', text)

def process_file(file_path):
    """Remove emojis from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove emojis
        new_content = remove_emojis_from_text(content)

        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to remove emojis from all project files."""
    project_root = Path('.')

    # File extensions to process
    extensions = ['.py', '.md', '.txt', '.yml', '.yaml', '.toml']

    # Directories to skip
    skip_dirs = {'.git', '.venv', '__pycache__', '.pytest_cache', 'node_modules', '.ipynb_checkpoints'}

    files_processed = []
    files_modified = []

    print("Scanning project for emojis...")

    for file_path in project_root.rglob('*'):
        # Skip directories
        if file_path.is_dir():
            continue

        # Skip if in excluded directory
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            continue

        # Process only specified extensions
        if file_path.suffix not in extensions:
            continue

        files_processed.append(file_path)

        if process_file(file_path):
            files_modified.append(file_path)
            print(f"  Modified: {file_path}")

    print(f"\nSummary:")
    print(f"  Files scanned: {len(files_processed)}")
    print(f"  Files modified: {len(files_modified)}")

    if files_modified:
        print(f"\nModified files:")
        for f in files_modified:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
