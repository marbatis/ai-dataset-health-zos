from pathlib import Path

from health import compute_health


def test_compute_health_reports_zero_byte(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "empty.bin").touch()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "ignored.txt").touch()

    report = compute_health(tmp_path)

    assert report.total_files == 2
    assert report.zero_byte_files == ["empty.bin"]
    assert report.score == 50


def test_compute_health_empty_directory(tmp_path: Path) -> None:
    report = compute_health(tmp_path)

    assert report.total_files == 0
    assert report.zero_byte_files == []
    assert report.score == 0
