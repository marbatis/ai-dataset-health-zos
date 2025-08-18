#!/usr/bin/env python3
"""
AI Dataset Health z/OS — repository file utilities and CLI.

- list_repository_files(): list files (relative to repo root), skipping .git/
- CLI: by default prints files; with --health prints an "empty-file" health score
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable


def list_repository_files(repo_path: str | Path | None = None) -> list[str]:
    """
    Return a sorted list of file paths (relative to repo root), skipping .git/.

    Args:
        repo_path: Path to the repository root. If None, uses current working dir.

    """
    root = Path(repo_path) if repo_path is not None else Path.cwd()
    root = root.resolve()

    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git directory in-place so os.walk doesn't descend into it
        if ".git" in dirnames:
            dirnames.remove(".git")

        for fname in filenames:
            rel = str((Path(dirpath) / fname).relative_to(root))
            files.append(rel)

    return sorted(files)


def compute_health(files: Iterable[str], root: Path) -> tuple[float, int, int]:
    """
    Compute a simple health score based on the proportion of non-empty files.

    Returns:
        (score_percent, empty_file_count, total_file_count)
    """
    file_list = list(files)
    total = len(file_list)
    if total == 0:
        return (100.0, 0, 0)

    empty = 0
    for rel in file_list:
        try:
            if (root / rel).stat().st_size == 0:
                empty += 1
        except FileNotFoundError:
            # If a file disappears between listing and stat, treat as empty
            empty += 1

    score = (total - empty) / total * 100.0
    return (score, empty, total)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="List repository files (skips .git); optionally report health."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Repository root to scan (defaults to current working directory).",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Report health score (based on empty-file count) instead of listing.",
    )

    args = parser.parse_args(argv)

    target: Path = (
        Path(args.path).resolve() if args.path is not None else Path.cwd().resolve()
    )

    files: list[str] = list_repository_files(target)

    if args.health:
        score, empty, total = compute_health(files, target)
        print(f"Health score: {score:.1f}%")
        print(f"Zero-byte files: {empty}")
        print(f"Total files: {total}")
        return 0

    # Default: print listing
    print(f"Listing files in repository: {target}")
    print("-" * 50)
    for i, rel in enumerate(files, start=1):
        print(f"{i:2}. {rel}")
    print(f"\nTotal files: {len(files)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - keep CLI robust
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
