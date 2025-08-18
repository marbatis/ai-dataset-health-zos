from pathlib import Path
import sys
import pytest

from list_files import list_repository_files, main


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


def test_nonexistent_repo_returns_empty(tmp_path: Path) -> None:
    missing = tmp_path / "missing"
    assert list_repository_files(missing) == []


def test_filters_and_depth(tmp_path: Path) -> None:
    (tmp_path / "keep.py").write_text("k")
    (tmp_path / "skip.log").write_text("s")
    (tmp_path / ".hidden").write_text("h")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "keep.txt").write_text("k")
    (tmp_path / "sub" / "skip.md").write_text("s")
    files = list_repository_files(
        tmp_path,
        include=["*.py", "sub/*"],
        exclude=["*.log", "sub/*.md"],
        max_depth=2,
    )
    assert files == ["keep.py", "sub/keep.txt"]


def test_main_success(
    sample_repo: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "argv", ["list_files.py", str(sample_repo)])
    main()
    out = capsys.readouterr().out
    assert "Listing files in repository" in out
    assert "Total files: 2" in out


def test_main_missing_path(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "argv", ["list_files.py", "does-not-exist"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "Path does not exist" in err
