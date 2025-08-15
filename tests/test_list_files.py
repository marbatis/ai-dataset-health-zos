from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from list_files import list_repository_files



from list_files import list_repository_files
def test_list_repository_files_excludes_git_and_is_sorted(tmp_path):
    (tmp_path / "a.txt").write_text("A")
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "b.txt").write_text("B")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("")

    files = list_repository_files(tmp_path)

    assert files == ["a.txt", "dir/b.txt"]


def test_list_repository_files_defaults_to_current_directory(tmp_path, monkeypatch):
    (tmp_path / "file.txt").write_text("")
    monkeypatch.chdir(tmp_path)
    assert list_repository_files() == ["file.txt"]
