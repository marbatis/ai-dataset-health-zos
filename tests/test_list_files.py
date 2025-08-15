from pathlib import Path
import pytest

from list_files import list_repository_files


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    # create repo contents
    (tmp_path / ".git" / "objects").mkdir(parents=True)
    (tmp_path / ".git" / "HEAD").write_text("ref: HEAD\n")
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "b.txt").write_text("b\n")
    (tmp_path / "z.txt").write_text("z\n")
    return tmp_path


def test_lists_sorted_and_skips_git(sample_repo: Path) -> None:
    files = list_repository_files(sample_repo)
    assert files == ["a/b.txt", "z.txt"]


def test_defaults_to_cwd(sample_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(sample_repo)
    files = list_repository_files()
    assert files == ["a/b.txt", "z.txt"]