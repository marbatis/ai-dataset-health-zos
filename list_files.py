#!/usr/bin/env python3
"""AI Dataset Health ZOS - File Listing Tool.

This script lists files in the repository for the AI dataset health scoring tool
for IBM z/OS via z/0SMF.
"""

from pathlib import Path, PurePosixPath
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

    if max_depth is not None and max_depth < 0:
        max_depth = None

    base_exclude = [".git/**"]
    patterns_exclude = base_exclude + (exclude or [])

    def _matches_pattern(
        posix_path: PurePosixPath, rel_path: str, pattern: str
    ) -> bool:
        """Return True if ``pattern`` matches ``rel_path``."""
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if rel_path == prefix or rel_path.startswith(prefix + "/"):
    def _matches_double_star_pattern(rel_path: str, pattern: str) -> bool:
        """Return True if ``pattern`` ending with '/**' matches ``rel_path``."""
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            return rel_path == prefix or rel_path.startswith(prefix + "/")
        return False

    def _matches_pattern(
        posix_path: PurePosixPath, rel_path: str, pattern: str
    ) -> bool:
        """Return True if ``pattern`` matches ``rel_path``."""
        if _matches_double_star_pattern(rel_path, pattern):
            return True
        if posix_path.match(pattern):
            return True
        if pattern.startswith("**/") and posix_path.match(pattern[3:]):
            return True
        return False

    def _match_any(rel_path: str, patterns: list[str]) -> bool:
        posix_path = PurePosixPath(rel_path)
        for pattern in patterns:
            if _matches_pattern(posix_path, rel_path, pattern):
                return True
        return False

    files: list[str] = []
    root_depth = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_depth = len(current.parts) - root_depth
        if max_depth is not None and rel_depth >= max_depth:
            dirnames[:] = []
        if include_hidden:
            dirnames[:] = [d for d in dirnames if d != ".git"]
        else:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        for filename in filenames:
            if not include_hidden and filename.startswith("."):
                continue
            path = Path(dirpath, filename)
            # Only check symlinks if exclude_symlinks_outside_root is True.
            if exclude_symlinks_outside_root and path.is_symlink():
                try:
                    path.resolve().relative_to(root)
                except ValueError:
                    continue
            rel_path = path.relative_to(root).as_posix()
            if include and not _match_any(rel_path, include):
                continue
            if _match_any(rel_path, patterns_exclude):
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
