from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Optional


@dataclass(frozen=True)
class HealthReport:
    total_files: int
    zero_byte_files: list[str]
    score: int


def _compute_health_fallback(root: Path) -> HealthReport:
    zero: list[str] = []
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for fn in filenames:
            p = Path(dirpath) / fn
            total += 1
            try:
                if p.stat().st_size == 0:
                    zero.append(p.relative_to(root).as_posix())
            except OSError:
                # Ignore unusual I/O errors in fallback
                continue
    zero.sort()
    score = 0 if total == 0 else 100 - round(100 * len(zero) / total)
    return HealthReport(total, zero, score)


try:
    # Prefer the top-level module present in this repo
    from health import compute_health as _compute_health  # type: ignore
except Exception:
    _compute_health = None  # type: ignore[assignment]


def compute_health_dispatch(root: Path) -> HealthReport:
    if _compute_health is not None:
        return _compute_health(root)  # type: ignore[misc]
    return _compute_health_fallback(root)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ai-dataset-health-zos",
        description="AI Dataset Health for z/OS via z/OSMF",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to repository root (default: current directory)",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Compute health for PATH and print summary",
    )
    args = parser.parse_args(argv)

    if not args.health:
        parser.print_help()
        return 0

    root = Path(args.path)
    try:
        if not root.exists():
            print(f"Path does not exist: {args.path}", file=sys.stderr)
            return 1
    except OSError as exc:
        print(f"Cannot access path {args.path!r}: {exc}", file=sys.stderr)
        return 1

    report = compute_health_dispatch(root)
    print(f"Health for: {root.resolve()}")
    print("-" * 50)
    print(f"Total files: {report.total_files}")
    print(f"Zero-byte files: {len(report.zero_byte_files)}")
    if report.zero_byte_files:
        print("Zero-byte list:")
        for rel in report.zero_byte_files:
            print(f" - {rel}")
    print(f"Score: {report.score}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
