from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HealthReport:
    total_files: int
    zero_byte_files: list[str]
    score: int


def compute_health(root: Path) -> HealthReport:
    """
    Empty-file based health score for a repository root.

    Scans all regular files under `root`, skipping any directory named '.git'.
    Score = 0 if no files, else 100 - round(100 * zero_count / total).
    """
    root = root.resolve()
    zero_byte_files: list[str] = []
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # prune .git at traversal level (exact match)
        if ".git" in dirnames:
            dirnames.remove(".git")

        for filename in filenames:
            p = Path(dirpath) / filename
            total_files += 1
            try:
                if p.stat().st_size == 0:
                    zero_byte_files.append(p.relative_to(root).as_posix())
            except OSError as exc:  # pragma: no cover — unusual I/O
                # compute a safe relative string for logging
                try:
                    rel = p.relative_to(root).as_posix()
                except Exception:
                    rel = str(p)
                logger.warning("Could not stat file %s: %s", rel, exc)

    zero_byte_files.sort()
    score = (
        0 if total_files == 0 else 100 - round(100 * len(zero_byte_files) / total_files)
    )
    return HealthReport(
        total_files=total_files, zero_byte_files=zero_byte_files, score=score
    )
