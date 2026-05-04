import unicode_to_png as utp


def test_read_version_reads_root_version_file(monkeypatch, tmp_path):
    script_path = tmp_path / "unicode_to_png.py"
    version_path = tmp_path / "VERSION"
    script_path.write_text("", encoding="utf-8")
    version_path.write_text("9.8.7\n", encoding="utf-8")

    monkeypatch.setattr(utp, "__file__", str(script_path))

    assert utp.read_version() == "9.8.7"


def test_read_version_returns_fallback_when_version_file_is_missing(monkeypatch, tmp_path):
    script_path = tmp_path / "unicode_to_png.py"
    script_path.write_text("", encoding="utf-8")

    monkeypatch.setattr(utp, "__file__", str(script_path))

    assert utp.read_version() == "0.0.0"


def test_sanitize_folder_name_keeps_alphanumeric_and_underscores():
    assert utp.sanitize_folder_name("release_pack_2026") == "release_pack_2026"


def test_sanitize_folder_name_replaces_each_unsafe_character():
    assert utp.sanitize_folder_name(" fire pack! #1 ") == "fire_pack___1"


def test_parse_batch_returns_pairs_with_aliases_without_warnings():
    pairs, warnings = utp.parse_batch("🔥:fire,🎯:target")

    assert pairs == [("🔥", "fire"), ("🎯", "target")]
    assert warnings == []


def test_parse_batch_uses_fallback_alias_for_missing_alias():
    pairs, warnings = utp.parse_batch("🎯")

    assert pairs == [("🎯", "emoji1")]
    assert warnings == ["Batch entry 1 has no alias. Fallback alias 'emoji1' was used."]


def test_parse_batch_skips_empty_entries_and_continues():
    pairs, warnings = utp.parse_batch(",🎯")

    assert pairs == [("🎯", "emoji1")]
    assert warnings == [
        "Skipped batch entry 1 because the emoji value is empty or not printable.",
        "Batch entry 2 has no alias. Fallback alias 'emoji1' was used.",
    ]


def test_parse_batch_uses_fallback_when_alias_sanitizes_to_empty():
    pairs, warnings = utp.parse_batch("🎯:!!!")

    assert pairs == [("🎯", "emoji1")]
    assert warnings == ["Batch entry 1 alias was empty after sanitization. Fallback alias 'emoji1' was used."]


def test_classify_unicode_structure_detects_simple_emoji():
    assert utp.classify_unicode_structure("🧱") == "SIMPLE"


def test_classify_unicode_structure_detects_skin_modifier():
    assert utp.classify_unicode_structure("👍🏽") == "SKIN_MODIFIER"


def test_classify_unicode_structure_detects_presentation_selector():
    assert utp.classify_unicode_structure("✏️") == "PRESENTATION_SELECTOR"


def test_classify_unicode_structure_detects_zwj_sequence():
    assert utp.classify_unicode_structure("👨‍💻") == "ZWJ_SEQUENCE"


def test_classify_unicode_structure_detects_regional_flag():
    assert utp.classify_unicode_structure("🇨🇱") == "REGIONAL_FLAG"


def test_classify_unicode_structure_returns_complex_for_unrecognized_multiple_codepoints():
    assert utp.classify_unicode_structure("ab") == "COMPLEX"


def test_get_adjusted_margin_uses_structure_boost():
    assert utp.get_adjusted_margin("ZWJ_SEQUENCE", 0.25, 100) == 37


def test_get_adjusted_margin_has_no_boost_for_simple_emoji():
    assert utp.get_adjusted_margin("SIMPLE", 0.25, 100) == 25


def test_console_message_uses_standard_prefix_and_uppercase_level():
    assert utp.console_message("warning", "Example warning.") == "[utp] - WARNING - Example warning."
