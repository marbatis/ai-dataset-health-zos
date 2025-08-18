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
    """Compute basic health metrics for files under ``root``.

    Files within any ``.git`` directory are ignored. Paths are returned as
    sorted, relative POSIX strings.
    """
    root = root.resolve()
    files: list[str] = []
    zero_byte_files: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git directories
        dirnames[:] = [d for d in dirnames if d != ".git"]
        dir_path = Path(dirpath)
        for name in filenames:
            file_path = dir_path / name
            rel = file_path.relative_to(root).as_posix()
            try:
                size = file_path.stat().st_size
            except OSError as exc:
                logger.warning("Could not stat file %s: %s", rel, exc)
                continue
            files.append(rel)
            if size == 0:
                zero_byte_files.append(rel)

    files.sort()
    zero_byte_files.sort()
    total_files = len(files)
    score = (
        0 if total_files == 0 else max(0, 100 - round(100 * len(zero_byte_files) / total_files))
    )
    return HealthReport(total_files, zero_byte_files, score)
