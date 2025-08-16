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


def test_include_glob_only_txt(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.md").write_text("b")
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "c.txt").write_text("c")
    result = list_repository_files(tmp_path, include=["**/*.txt"])
    assert result == ["a.txt", "dir/c.txt"]


def test_exclude_dir_pattern(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.md").write_text("b")
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "c.txt").write_text("c")
    (tmp_path / "dir" / "skip").mkdir()
    (tmp_path / "dir" / "skip" / "me.log").write_text("x")
    result = list_repository_files(tmp_path, exclude=["dir/**"])
    assert result == ["a.txt", "b.md"]


def test_max_depth_limits_walk(tmp_path: Path) -> None:
    (tmp_path / "top.txt").write_text("t")
    (tmp_path / "d1").mkdir()
    (tmp_path / "d1" / "a.txt").write_text("a")
    (tmp_path / "d1" / "d2").mkdir()
    (tmp_path / "d1" / "d2" / "b.txt").write_text("b")
    result = list_repository_files(tmp_path, max_depth=1)
    assert result == ["d1/a.txt", "top.txt"]


def test_hidden_files_default_and_opt_in(tmp_path: Path) -> None:
    (tmp_path / ".secret").write_text("s")
    (tmp_path / ".hidden").mkdir()
    (tmp_path / ".hidden" / "file.txt").write_text("h")
    (tmp_path / "visible.txt").write_text("v")
    assert list_repository_files(tmp_path) == ["visible.txt"]
    assert list_repository_files(tmp_path, include_hidden=True) == [
        ".hidden/file.txt",
        ".secret",
        "visible.txt",
    ]
