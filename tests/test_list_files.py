from pathlib import Path
import pytest

from list_files import list_repository_files


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "ignored.txt").write_text("x")
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "b.txt").write_text("b")
    return tmp_path


def test_lists_sorted_relative_paths(sample_repo: Path) -> None:
    files = list_repository_files(sample_repo)
    assert files == ["a.txt", "dir/b.txt"]


def test_defaults_to_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "one").write_text("1")
    (tmp_path / "two").write_text("2")
    monkeypatch.chdir(tmp_path)
    assert sorted(list_repository_files()) == ["one", "two"]

