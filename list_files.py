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
import traceback
from pathlib import Path

from health import HealthReport, compute_health


def list_repository_files(
    repo_path: str | Path = ".",
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    max_depth: int | None = None,
    include_hidden: bool = False,
) -> list[str]:
    """List files under ``repo_path`` as sorted, relative POSIX paths, with filtering.

    - ``include``: keep only paths matching ANY glob (Path.match on relative POSIX).
    - ``exclude``: drop paths matching ANY glob; wins over include.
    - Always excludes .git/**.
    - ``max_depth``: 0 = only files at root; 1 = root and one level below; etc.
    - ``include_hidden``: if False, skip entries starting with '.' (files/dirs).
    """
    root = Path(repo_path).resolve()
    if not root.exists():
        return []

    base_exclude = {".git/**"}
    inc = [p for p in (include or []) if p] or None
    exc = list(base_exclude | set(exclude or []))
    depth_limit = None if (max_depth is None or max_depth < 0) else int(max_depth)

    def is_hidden_part(p: Path) -> bool:
        return any(part.startswith(".") for part in p.parts)

    out: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        rel_dir = dir_path.relative_to(root)

        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        if depth_limit is not None:
            current_depth = len(rel_dir.parts)
            if current_depth >= depth_limit:
                dirnames[:] = []

        pruned = []
        for d in dirnames:
            rel_d = (rel_dir / d).as_posix()
            if any(
                Path(rel_d).match(p.rstrip("/")) or Path(rel_d + "/").match(p)
                for p in exc
            ):
                continue
            pruned.append(d)
        dirnames[:] = pruned

        for fn in filenames:
            file_path = dir_path / fn
            rel = file_path.relative_to(root).as_posix()

            if not include_hidden and is_hidden_part(Path(rel)):
                continue

            if inc is not None and not any(Path(rel).match(p) for p in inc):
                continue

            if any(Path(rel).match(p) for p in exc):
                continue

            out.append(rel)

    out.sort()
    return out


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

    repo_path = Path(args.path) if args.path is not None else None
    if repo_path is not None:
        try:
            if not repo_path.exists():
                print(f"Path does not exist: {args.path}", file=sys.stderr)
                raise SystemExit(1)
        except OSError as exc:
            print(f"Cannot access path {args.path!r}: {exc}", file=sys.stderr)
            raise SystemExit(1)

    target = repo_path or Path.cwd()

    if args.health:
        report: HealthReport = compute_health(target)
        score = 100.0 if report.total_files == 0 else float(report.score)
        print(f"Health score: {score:.1f}%")
        print(f"Zero-byte files: {len(report.zero_byte_files)}")
        print(f"Total files: {report.total_files}")
        return 0

    print(f"Listing files in repository: {target.resolve()}")
    print("-" * 50)

    files: list[str] = list_repository_files(repo_path or Path.cwd())

    if files:
        for i, file_path in enumerate(files, 1):
            print(f"{i:2}. {file_path}")
        print(f"\nTotal files: {len(files)}")
    else:
        print("No files found in the repository.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:  # noqa: BLE001 - keep CLI robust
        traceback.print_exc()
        raise SystemExit(1)
