#!/usr/bin/env python3
"""AI Dataset Health ZOS - File Listing Tool.

This script lists files in the repository for the AI dataset health scoring tool
for IBM z/OS via z/0SMF.
"""

from pathlib import Path
import os
import sys


def list_repository_files(
    repo_path: str | Path = ".",
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    max_depth: int | None = None,
    include_hidden: bool = False,
) -> list[str]:
    """Return sorted relative file paths within ``repo_path``.

    Args:
        repo_path: Repository root. Defaults to current working directory.
        include: Glob patterns to include. Keep files matching any pattern.
        exclude: Glob patterns to exclude. ``".git/**"`` is always excluded.
        max_depth: Maximum directory depth to traverse relative to ``repo_path``.
        include_hidden: Include files and directories starting with ``.``.
    """
    root = Path(repo_path).resolve()
    if not root.exists():
        return []

    if not include:
        include = None
    if max_depth is not None and max_depth < 0:
        max_depth = None

    base_exclude = [".git/**"]
    patterns_exclude = base_exclude + (exclude or [])

    def _match_any(path_obj: Path, patterns: list[str]) -> bool:
        posix = path_obj.as_posix()
        for pattern in patterns:
            if pattern.endswith("/**"):
                prefix = pattern[:-3]
                if posix == prefix or posix.startswith(prefix + "/"):
                    return True
            if path_obj.match(pattern) or (
                pattern.startswith("**/") and path_obj.match(pattern[3:])
            ):
                return True
        return False

    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        depth = len(rel_dir.parts)
        if max_depth is not None and depth >= max_depth:
            dirnames[:] = []
        if include_hidden:
            dirnames[:] = [d for d in dirnames if d != ".git"]
        else:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        for filename in filenames:
            if not include_hidden and filename.startswith("."):
                continue
            rel_path = Path(dirpath, filename).relative_to(root).as_posix()
            path_obj = Path(rel_path)
            if include and not _match_any(path_obj, include):
                continue
            if _match_any(path_obj, patterns_exclude):
                continue
            files.append(rel_path)

    return sorted(files)


def main():
    """Main function to list repository files."""
    repo_arg = sys.argv[1] if len(sys.argv) > 1 else None
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
        target = repo_path or Path.cwd()
        print(f"Listing files in repository: {target.resolve()}")
        print("-" * 50)

        files = list_repository_files(target)

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
