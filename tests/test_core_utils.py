#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
from pathlib import Path

from unicode_to_png.logging_utils import console_message
from unicode_to_png.logging_utils import write_log_if_needed
from unicode_to_png.path_utils import prepare_log_path, sanitize_folder_name
from unicode_to_png.unicode_utils import classify_unicode_structure, get_adjusted_margin
from unicode_to_png.version import read_version
from unicode_to_png import parse_batch


SAMPLE_LOG_ENTRY = "[TEST] Example event."
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_read_version_reads_root_version_file(tmp_path):
    version_path = tmp_path / "VERSION"
    version_path.write_text("9.8.7\n", encoding="utf-8")

    assert read_version(root_dir=tmp_path) == "9.8.7"


def test_read_version_returns_fallback_when_version_file_is_missing(tmp_path):
    assert read_version(root_dir=tmp_path) == "0.0.0"


def test_project_metadata_version_matches_version_file():
    version = (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert f'version = "{version}"' in pyproject


def test_sanitize_folder_name_keeps_alphanumeric_and_underscores():
    assert sanitize_folder_name("release_pack_2026") == "release_pack_2026"


def test_sanitize_folder_name_replaces_each_unsafe_character():
    assert sanitize_folder_name(" fire pack! #1 ") == "fire_pack___1"


def test_parse_batch_returns_pairs_with_aliases_without_warnings():
    pairs, warnings = parse_batch("🔥:fire,🎯:target")

    assert pairs == [("🔥", "fire"), ("🎯", "target")]
    assert warnings == []


def test_parse_batch_uses_fallback_alias_for_missing_alias():
    pairs, warnings = parse_batch("🎯")

    assert pairs == [("🎯", "emoji1")]
    assert warnings == ["Batch entry 1 has no alias. Fallback alias 'emoji1' was used."]


def test_parse_batch_skips_empty_entries_and_continues():
    pairs, warnings = parse_batch(",🎯")

    assert pairs == [("🎯", "emoji1")]
    assert warnings == [
        "Skipped batch entry 1 because the emoji value is empty or not printable.",
        "Batch entry 2 has no alias. Fallback alias 'emoji1' was used.",
    ]


def test_parse_batch_skips_invalid_non_emoji_entries_and_continues():
    pairs, warnings = parse_batch("abc:invalid,🎯:target")

    assert pairs == [("🎯", "target")]
    assert warnings == ["Skipped batch entry 1 because 'abc' is not a valid emoji."]


def test_parse_batch_uses_fallback_when_alias_sanitizes_to_empty():
    pairs, warnings = parse_batch("🎯:!!!")

    assert pairs == [("🎯", "emoji1")]
    assert warnings == ["Batch entry 1 alias was empty after sanitization. Fallback alias 'emoji1' was used."]


def test_classify_unicode_structure_detects_simple_emoji():
    assert classify_unicode_structure("🧱") == "SIMPLE"


def test_classify_unicode_structure_detects_skin_modifier():
    assert classify_unicode_structure("👍🏽") == "SKIN_MODIFIER"


def test_classify_unicode_structure_detects_presentation_selector():
    assert classify_unicode_structure("✏️") == "PRESENTATION_SELECTOR"


def test_classify_unicode_structure_detects_zwj_sequence():
    assert classify_unicode_structure("👨‍💻") == "ZWJ_SEQUENCE"


def test_classify_unicode_structure_detects_regional_flag():
    assert classify_unicode_structure("🇨🇱") == "REGIONAL_FLAG"


def test_classify_unicode_structure_returns_complex_for_unrecognized_multiple_codepoints():
    assert classify_unicode_structure("ab") == "COMPLEX"


def test_get_adjusted_margin_uses_structure_boost():
    assert get_adjusted_margin("ZWJ_SEQUENCE", 0.25, 100) == 37


def test_get_adjusted_margin_has_no_boost_for_simple_emoji():
    assert get_adjusted_margin("SIMPLE", 0.25, 100) == 25


def test_console_message_uses_standard_prefix_and_uppercase_level():
    assert console_message("warning", "Example warning.") == "[utp] - WARNING - Example warning."


def test_prepare_log_path_returns_none_when_log_directory_cannot_be_created(tmp_path, monkeypatch):
    def raise_os_error(*args, **kwargs):
        raise OSError("simulated directory failure")

    monkeypatch.setattr("unicode_to_png.path_utils.os.makedirs", raise_os_error)

    assert prepare_log_path(tmp_path, "codex_log_failure") is None


def test_write_log_if_needed_returns_true_without_entries(tmp_path):
    log_file = tmp_path / "runtime.log"

    assert write_log_if_needed([], log_file) is True
    assert not log_file.exists()


def test_write_log_if_needed_persists_entries(tmp_path):
    log_file = tmp_path / "runtime.log"

    assert write_log_if_needed([SAMPLE_LOG_ENTRY], log_file) is True
    assert "Example event." in log_file.read_text(encoding="utf-8")


def test_write_log_if_needed_warns_when_log_path_is_unavailable(capsys):
    assert write_log_if_needed([SAMPLE_LOG_ENTRY], None) is False

    output = capsys.readouterr().out
    assert "[utp] - WARNING - Log file path is unavailable. Runtime log entries were not persisted." in output


def test_write_log_if_needed_warns_when_log_file_cannot_be_written(tmp_path, capsys):
    blocked_log_path = tmp_path / "blocked"
    blocked_log_path.mkdir()

    assert write_log_if_needed([SAMPLE_LOG_ENTRY], blocked_log_path) is False

    output = capsys.readouterr().out
    assert f"[utp] - WARNING - Failed to write runtime log file: {blocked_log_path}." in output
    assert "[utp] - WARNING - Log persistence error detail:" in output
