import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "unicode_to_png.py"
EMOJIS_ROOT = PROJECT_ROOT / "emojis"
LOG_ROOT = PROJECT_ROOT / "log"
ICON_SIZES = (16, 19, 32, 38, 48, 128)


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


def cleanup_codex_artifacts(*folder_names):
    for folder_name in folder_names:
        shutil.rmtree(EMOJIS_ROOT / folder_name, ignore_errors=True)

    if LOG_ROOT.exists():
        for folder_name in folder_names:
            for log_file in LOG_ROOT.glob(f"*{folder_name}.log"):
                log_file.unlink(missing_ok=True)


def assert_valid_icon_set(output_folder):
    for size in ICON_SIZES:
        icon_path = output_folder / f"emoji_{size}x{size}.png"
        assert icon_path.exists()
        assert icon_path.stat().st_size > 0

        with Image.open(icon_path) as icon:
            assert icon.format == "PNG"
            assert icon.size == (size, size)
            assert icon.mode == "RGBA"
            assert icon.getchannel("A").getbbox() is not None


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


def test_cli_without_input_arguments_exits_without_interactive_prompt():
    result = run_cli("--quiet")

    assert result.returncode == 1
    assert "[utp] - ERROR - No emoji input was provided. Use --emoji or --batch." in result.stdout
    assert "Enter the emoji symbol:" not in result.stdout
    assert result.stderr == ""


def test_cli_without_folder_argument_exits_without_interactive_prompt():
    result = run_cli("--emoji", "😀", "--quiet")

    assert result.returncode == 1
    assert "[utp] - ERROR - No output folder name was provided. Use --folder." in result.stdout
    assert "Folder name to save icons" not in result.stdout
    assert result.stderr == ""


def test_cli_batch_without_valid_entries_exits_before_rendering():
    result = run_cli("--batch", ",", "--folder", "cli_empty_batch", "--quiet")

    assert result.returncode == 1
    assert "[utp] - ERROR - No valid emoji entries were provided." in result.stdout
    assert result.stderr == ""
    assert not (PROJECT_ROOT / "emojis" / "cli_empty_batch").exists()


def test_cli_generates_valid_png_icon_set_for_single_emoji():
    folder_name = "codex_integration_single"
    cleanup_codex_artifacts(folder_name)

    try:
        result = run_cli("--emoji", "😀", "--folder", folder_name, "--quiet")

        assert result.returncode == 0
        assert result.stderr == ""
        assert_valid_icon_set(EMOJIS_ROOT / folder_name)
    finally:
        cleanup_codex_artifacts(folder_name)


def test_cli_generates_valid_png_icon_sets_for_batch_argument():
    folder_base = "codex_integration_batch"
    output_folders = (f"{folder_base}_fire", f"{folder_base}_target")
    cleanup_codex_artifacts(*output_folders)

    try:
        result = run_cli(
            "--batch",
            "🔥:fire,🎯:target",
            "--folder",
            folder_base,
            "--quiet",
        )

        assert result.returncode == 0
        assert result.stderr == ""
        for output_folder in output_folders:
            assert_valid_icon_set(EMOJIS_ROOT / output_folder)
    finally:
        cleanup_codex_artifacts(*output_folders)
