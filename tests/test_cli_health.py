from pathlib import Path
import sys

import pytest

from list_files import main


def test_cli_health_reports(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "empty.bin").touch()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "ignored.txt").write_text("ignore")
    monkeypatch.setattr(sys, "argv", ["list_files.py", "--health", str(tmp_path)])
    main()
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "Health score: 50",
        "Zero-byte files (1):",
        "  - empty.bin",
        "Total files scanned: 2",
    ]
    assert "Listing files in repository" not in captured.out


def test_cli_health_empty(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "argv", ["list_files.py", "--health", str(tmp_path)])
    main()
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "Health score: 0",
        "Zero-byte files (0):",
        "Total files scanned: 0",
    ]
    assert "Listing files in repository" not in captured.out
