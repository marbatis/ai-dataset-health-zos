from pathlib import Path
import subprocess
import sys


def test_cli_health_flag_works():
    """Test that the CLI health flag actually works."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_dataset_health_zos.cli", "--health", "."],
        cwd=Path(__file__).parent.parent,
        env={"PYTHONPATH": str(Path(__file__).parent.parent / "src")},
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    assert "Health for:" in result.stdout
    assert "Score:" in result.stdout
    assert "Total files:" in result.stdout


def test_cli_without_health_shows_help():
    """Test that CLI without --health flag shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_dataset_health_zos.cli", "."],
        cwd=Path(__file__).parent.parent,
        env={"PYTHONPATH": str(Path(__file__).parent.parent / "src")},
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower() or "AI Dataset Health" in result.stdout


def test_cli_nonexistent_path():
    """Test CLI with non-existent path returns error."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_dataset_health_zos.cli", "--health", "/nonexistent/path"],
        cwd=Path(__file__).parent.parent,
        env={"PYTHONPATH": str(Path(__file__).parent.parent / "src")},
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 1
    assert "does not exist" in result.stderr.lower()
