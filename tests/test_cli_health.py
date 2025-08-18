from pathlib import Path

import pytest

from list_files import main


def test_cli_health_reports(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "empty.bin").touch()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "ignored.txt").write_text("ignore")
    main(["--health", str(tmp_path)])
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "Health score: 50.0%",
        "Zero-byte files: 1",
        "Total files: 2",
    ]
    assert "Listing files in repository" not in captured.out


def test_cli_health_empty(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    main(["--health", str(tmp_path)])
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "Health score: 100.0%",
        "Zero-byte files: 0",
        "Total files: 0",
    ]
    assert "Listing files in repository" not in captured.out
