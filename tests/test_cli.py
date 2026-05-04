import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "unicode_to_png.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_cli_help_returns_usage_without_runtime_dependency_checks():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "usage: unicode_to_png.py" in result.stdout
    assert "--version" in result.stdout
    assert result.stderr == ""


def test_cli_version_reads_version_file():
    expected_version = (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip()

    result = run_cli("--version")

    assert result.returncode == 0
    assert result.stdout.strip() == f"unicode_to_png {expected_version}"
    assert result.stderr == ""


def test_cli_invalid_emoji_exits_with_objective_error_message():
    result = run_cli("--emoji", "abc", "--folder", "cli_invalid_input", "--quiet")

    assert result.returncode == 1
    assert "[utp] - ERROR - Invalid emoji input: 'abc'." in result.stdout
    assert result.stderr == ""


def test_cli_batch_without_valid_entries_exits_before_rendering():
    result = run_cli("--batch", ",", "--folder", "cli_empty_batch", "--quiet")

    assert result.returncode == 1
    assert "[utp] - ERROR - No valid emoji entries were provided." in result.stdout
    assert result.stderr == ""
    assert not (PROJECT_ROOT / "emojis" / "cli_empty_batch").exists()
