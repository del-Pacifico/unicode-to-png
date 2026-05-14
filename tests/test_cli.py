#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
import shutil
import subprocess
import sys
import importlib.util
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "unicode_to_png.py"
EMOJIS_ROOT = PROJECT_ROOT / "emojis"
LOG_ROOT = PROJECT_ROOT / "log"
_CLI_MODULE = None


def load_cli_module():
    global _CLI_MODULE
    if _CLI_MODULE is not None:
        return _CLI_MODULE
    spec = importlib.util.spec_from_file_location("unicode_to_png_cli", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _CLI_MODULE = module
    return _CLI_MODULE


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


def assert_valid_icon_set(output_folder, filename_prefix="emoji"):
    for size in load_cli_module().ICON_SIZES:
        icon_path = output_folder / f"{filename_prefix}_{size}x{size}.png"
        assert icon_path.exists()
        assert icon_path.stat().st_size > 0

        with Image.open(icon_path) as icon:
            assert icon.format == "PNG"
            assert icon.size == (size, size)
            assert icon.mode == "RGBA"
            assert icon.getchannel("A").getbbox() is not None


def test_check_visual_edges_reports_right_or_bottom_contact():
    cli_module = load_cli_module()
    image = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    image.putpixel((3, 1), (255, 255, 255, 255))

    log_entries = []

    assert cli_module.check_visual_edges(image, 4, log_entries, quiet=True) is True
    assert "Emoji touches right edge(s) at 4x4." in log_entries[0]


def test_check_visual_edges_returns_false_when_output_has_padding():
    cli_module = load_cli_module()
    image = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    image.putpixel((1, 1), (255, 255, 255, 255))

    log_entries = []

    assert cli_module.check_visual_edges(image, 4, log_entries, quiet=True) is False
    assert log_entries == []


def test_cli_help_returns_usage_without_runtime_dependency_checks():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "usage: unicode_to_png.py" in result.stdout
    assert "--version" in result.stdout
    assert "Usage rules:" in result.stdout
    assert "Examples:" in result.stdout
    assert "python unicode_to_png.py --emoji" in result.stdout
    assert "--filename-prefix" in result.stdout
    assert "python unicode_to_png.py --examples" in result.stdout
    assert result.stderr == ""


def test_cli_examples_returns_detailed_examples_without_runtime_dependency_checks():
    result = run_cli("--examples")

    assert result.returncode == 0
    assert "Unicode to PNG CLI examples" in result.stdout
    assert "Basic single emoji:" in result.stdout
    assert "Medium batch generation:" in result.stdout
    assert "Automatic edge correction:" in result.stdout
    assert "docs/USAGE.md" in result.stdout
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


def test_cli_batch_with_only_invalid_non_emoji_entries_exits_before_rendering():
    result = run_cli("--batch", "abc:invalid", "--folder", "cli_invalid_batch", "--quiet")

    assert result.returncode == 1
    assert "[utp] - WARNING - Skipped batch entry 1 because 'abc' is not a valid emoji." in result.stdout
    assert "[utp] - ERROR - No valid emoji entries were provided." in result.stdout
    assert result.stderr == ""
    assert not (PROJECT_ROOT / "emojis" / "cli_invalid_batch").exists()


def test_cli_rejects_conflicting_filename_prefix_options():
    result = run_cli(
        "--emoji",
        "😀",
        "--folder",
        "cli_conflicting_prefix",
        "--filename-prefix",
        "custom",
        "--filename-prefix-from-folder",
        "--quiet",
    )

    assert result.returncode == 1
    assert "[utp] - ERROR - Use either --filename-prefix or --filename-prefix-from-folder, not both." in result.stdout
    assert result.stderr == ""


def test_cli_rejects_empty_filename_prefix_after_sanitization():
    result = run_cli("--emoji", "😀", "--folder", "cli_empty_prefix", "--filename-prefix", "!!!", "--quiet")

    assert result.returncode == 1
    assert "[utp] - ERROR - Filename prefix '!!!' is empty after sanitization." in result.stdout
    assert result.stderr == ""


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


def test_cli_generates_valid_png_icon_set_with_custom_filename_prefix():
    folder_name = "codex_custom_prefix"
    filename_prefix = "chrome_icon"
    cleanup_codex_artifacts(folder_name)

    try:
        result = run_cli(
            "--emoji",
            "😀",
            "--folder",
            folder_name,
            "--filename-prefix",
            filename_prefix,
            "--quiet",
        )

        assert result.returncode == 0
        assert result.stderr == ""
        assert_valid_icon_set(EMOJIS_ROOT / folder_name, filename_prefix=filename_prefix)
        assert not (EMOJIS_ROOT / folder_name / "emoji_16x16.png").exists()
    finally:
        cleanup_codex_artifacts(folder_name)


def test_cli_generates_valid_png_icon_sets_with_folder_filename_prefix():
    folder_base = "codex_folder_prefix"
    output_folders = (f"{folder_base}_fire", f"{folder_base}_target")
    cleanup_codex_artifacts(*output_folders)

    try:
        result = run_cli(
            "--batch",
            "🔥:fire,🎯:target",
            "--folder",
            folder_base,
            "--filename-prefix-from-folder",
            "--quiet",
        )

        assert result.returncode == 0
        assert result.stderr == ""
        for output_folder in output_folders:
            assert_valid_icon_set(EMOJIS_ROOT / output_folder, filename_prefix=output_folder)
            assert not (EMOJIS_ROOT / output_folder / "emoji_16x16.png").exists()
    finally:
        cleanup_codex_artifacts(*output_folders)
