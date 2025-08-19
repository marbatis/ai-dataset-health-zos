from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import logging

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

    for p in root.rglob("*"):
        if p.is_dir():
            continue
        # Exclude files under .git/
        if any(part == ".git" for part in p.parts):
            continue

        total_files += 1
        try:
            if p.stat().st_size == 0:
                zero_byte_files.append(p.relative_to(root).as_posix())
        except OSError as exc:  # pragma: no cover - unusual I/O errors
            logger.warning("Could not stat file %s: %s", p.relative_to(root), exc)

    zero_byte_files.sort()
    score = (
        0 if total_files == 0 else 100 - round(100 * len(zero_byte_files) / total_files)
    )
    return HealthReport(
        total_files=total_files, zero_byte_files=zero_byte_files, score=score
    )
