#!/usr/bin/env python3
"""AI Dataset Health ZOS - File Listing Tool.

This script lists files in the repository for the AI dataset health scoring tool
for IBM z/OS via z/0SMF.
"""

from pathlib import Path
import sys


def list_repository_files(path: Path | None = None) -> list[str]:
    """Return sorted relative file paths within *path*, ignoring ``.git``.

    Args:
        path: Repository root. Defaults to :func:`pathlib.Path.cwd`.
    """
    if path is None:
        path = Path.cwd()

    files: list[str] = []
    for p in path.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            files.append(str(p.relative_to(path)))

    return sorted(files)


def main():
    """Main function to list repository files."""
    try:
        # Get repository path from command line or use current directory
        repo_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None

        target = repo_path or Path.cwd()
        print(f"Listing files in repository: {target.resolve()}")
        print("-" * 50)

        files = list_repository_files(repo_path)

        if files:
            for i, file_path in enumerate(files, 1):
                print(f"{i:2}. {file_path}")
            print(f"\nTotal files: {len(files)}")
        else:
            print("No files found in the repository.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
