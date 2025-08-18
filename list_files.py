#!/usr/bin/env python3
"""AI Dataset Health ZOS - File Listing Tool.

This script lists files in the repository for the AI dataset health scoring tool
for IBM z/OS via z/0SMF.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

from health import compute_health


def list_repository_files(
    repo_path: str | Path = ".",
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    max_depth: int | None = None,
    include_hidden: bool = False,
) -> list[str]:
    """List files under `repo_path` as sorted, relative POSIX paths, with filtering.

    - `include`: keep only paths matching ANY glob (Path.match on relative POSIX).
    - `exclude`: drop paths matching ANY glob; wins over include.
    - Always excludes .git/**.
    - `max_depth`: 0 = only files at root; 1 = root and one level below; etc.
    - `include_hidden`: if False, skip entries starting with '.' (files/dirs).
    """
    root = Path(repo_path).resolve()
    if not root.exists():
        return []

    # Normalize args
    base_exclude = {".git/**"}
    inc = [p for p in (include or []) if p] or None
    exc = list(base_exclude | set(exclude or []))
    depth_limit = None if (max_depth is None or max_depth < 0) else int(max_depth)

    def is_hidden_part(p: Path) -> bool:
        # Any component that starts with '.' means "hidden"
        return any(part.startswith(".") for part in p.parts)

    out: list[str] = []

    # Use os.walk to prune traversal early (depth + excludes + hidden dirs)
    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        rel_dir = dir_path.relative_to(root)

        # Prune hidden dirs if include_hidden is False
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        # Prune by depth
        if depth_limit is not None:
            current_depth = len(rel_dir.parts)  # 0 at root
            # If we're already deeper than depth_limit, stop descending
            if current_depth >= depth_limit:
                dirnames[:] = []

        # Prune excludes on directories (avoid descending into excluded trees)
        # Apply patterns on POSIX rel path with a trailing slash for dirs
        pruned = []
        for d in dirnames:
            rel_d = (rel_dir / d).as_posix()
            # if excluded by any pattern like "dir/**", skip entering it
            if any(
                Path(rel_d).match(p.rstrip("/")) or Path(rel_d + "/").match(p)
                for p in exc
            ):
                continue
            pruned.append(d)
        dirnames[:] = pruned

        # Files in this directory
        for fn in filenames:
            file_path = dir_path / fn
            rel = file_path.relative_to(root).as_posix()

            if not include_hidden and is_hidden_part(Path(rel)):
                continue

            # include filter (if provided)
            if inc is not None and not any(Path(rel).match(p) for p in inc):
                continue

            # exclude filter (wins)
            if any(Path(rel).match(p) for p in exc):
                continue

            out.append(rel)

    out.sort()
    return out


def main() -> None:
    """List repository files or compute basic health metrics."""
    args = sys.argv[1:]
    health_flag = False
    repo_arg: str | None = None

    if args and args[0] == "--health":
        health_flag = True
        args = args[1:]

    if args:
        repo_arg = args[0]

    repo_path: Path | None = None
    if repo_arg is not None:
        repo_path = Path(repo_arg)
        try:
            if not repo_path.exists():
                print(f"Path does not exist: {repo_arg}", file=sys.stderr)
                sys.exit(1)
        except OSError as exc:
            print(f"Cannot access path {repo_arg!r}: {exc}", file=sys.stderr)
            sys.exit(1)

    try:
        target = (repo_path or Path.cwd()).resolve()
        if health_flag:
            report = compute_health(target)
            print(f"Health score: {report.score}")
            print(f"Zero-byte files ({len(report.zero_byte_files)}):")
            for name in report.zero_byte_files:
                print(f"  - {name}")
            print(f"Total files scanned: {report.total_files}")
            return

        print(f"Listing files in repository: {target}")
        print("-" * 50)

        files: list[str] = list_repository_files(repo_path or Path.cwd())

        if files:
            for i, file_path in enumerate(files, 1):
                print(f"{i:2}. {file_path}")
            print(f"\nTotal files: {len(files)}")
        else:
            print("No files found in the repository.")

    except Exception as exc:  # pragma: no cover - defensive
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
