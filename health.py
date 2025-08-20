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
    Compute a simple empty-file based health score for the given root.

    - total_files counts all regular files under root, excluding anything in .git/
    - zero_byte_files lists relative POSIX paths whose size is 0
    - score = 0 if total_files == 0 else 100 - round(100 * len(zero_byte_files) / total_files)
    """
    zero_byte_files: list[str] = []
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for fn in filenames:
            p = Path(dirpath) / fn
            total_files += 1
            try:
                if p.stat().st_size == 0:
                    zero_byte_files.append(p.relative_to(root).as_posix())
            except OSError as exc:  # pragma: no cover - unusual I/O errors
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
