from unicode_to_png.logging_utils import console_message
from unicode_to_png.path_utils import sanitize_folder_name
from unicode_to_png.unicode_utils import classify_unicode_structure, get_adjusted_margin
from unicode_to_png.version import read_version
from unicode_to_png import parse_batch


def test_read_version_reads_root_version_file(tmp_path):
    version_path = tmp_path / "VERSION"
    version_path.write_text("9.8.7\n", encoding="utf-8")

    assert read_version(root_dir=tmp_path) == "9.8.7"


def test_read_version_returns_fallback_when_version_file_is_missing(tmp_path):
    assert read_version(root_dir=tmp_path) == "0.0.0"


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
