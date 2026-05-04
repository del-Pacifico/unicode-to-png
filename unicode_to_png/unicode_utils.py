"""Unicode classification and layout helpers for emoji rendering."""

from .logging_utils import log


def is_emoji(character):
    """Validate whether a character belongs to common Unicode emoji ranges."""
    return any([
        "\U0001F300" <= character <= "\U0001F5FF",  # Misc Symbols and Pictographs
        "\U0001F600" <= character <= "\U0001F64F",  # Emoticons
        "\U0001F680" <= character <= "\U0001F6FF",  # Transport and Map Symbols
        "\U0001F700" <= character <= "\U0001F77F",  # Alchemical Symbols
        "\U0001F780" <= character <= "\U0001F7FF",  # Geometric Shapes Extended
        "\U0001F800" <= character <= "\U0001F8FF",  # Supplemental Arrows-C
        "\U0001F900" <= character <= "\U0001F9FF",  # Supplemental Symbols and Pictographs
        "\U0001FA00" <= character <= "\U0001FA6F",  # Extended-A
        "\U0001FA70" <= character <= "\U0001FAFF",  # Extended-B
        "\u2600" <= character <= "\u26FF",  # Misc symbols
        "\u2700" <= character <= "\u27BF",  # Dingbats
    ])


def classify_unicode_structure(emoji: str) -> str:
    """
    Classify the emoji into structural categories.

    Args:
        emoji (str): The emoji character string.

    Returns:
        str: Classification category.
    """
    try:
        codepoints = [ord(c) for c in emoji]

        # ZWJ-based sequence.
        if 0x200D in codepoints:
            return "ZWJ_SEQUENCE"

        # Base emoji with skin tone modifier.
        if any(0x1F3FB <= cp <= 0x1F3FF for cp in codepoints):
            return "SKIN_MODIFIER"

        # Emoji with presentation selector.
        if 0xFE0F in codepoints:
            return "PRESENTATION_SELECTOR"

        # Regional indicator flags.
        if all(0x1F1E6 <= cp <= 0x1F1FF for cp in codepoints):
            return "REGIONAL_FLAG"

        # Single code point emoji.
        if len(codepoints) == 1:
            return "SIMPLE"

        # Any unrecognized structure.
        return "COMPLEX"

    except Exception:
        return "COMPLEX"


def get_adjusted_margin(structure_type, base_ratio, size_px):
    """
    Calculate a structure-aware margin in pixels.

    Args:
        structure_type (str): Classification from classify_unicode_structure(...).
        base_ratio (float): User-defined or default margin ratio.
        size_px (int): Canvas size in pixels.

    Returns:
        int: Total margin in pixels.
    """
    boost = {
        "SKIN_MODIFIER": 0.10,
        "PRESENTATION_SELECTOR": 0.08,
        "ZWJ_SEQUENCE": 0.12,
        "REGIONAL_FLAG": 0.06,
        "COMPLEX": 0.15,
    }.get(structure_type, 0.0)

    total_ratio = base_ratio + boost
    return int(size_px * total_ratio)


def get_adjusted_position(structure_type, temp_size, bbox, log_entries, quiet):
    """
    Return corrected coordinates for drawing emoji, compensating for Unicode type.

    Args:
        structure_type (str): Classification from classify_unicode_structure(...).
        temp_size (int): Base canvas size.
        bbox (tuple): Bounding box from draw.textbbox().
        log_entries (list): Log collection.
        quiet (bool): Suppress console output.

    Returns:
        tuple: (x, y) coordinates.
    """
    try:
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        x = (temp_size - width) // 2 - bbox[0]
        y = (temp_size - height) // 2 - bbox[1]

        # Vertical lift applied by structure type.
        y_lift = {
            "SKIN_MODIFIER": 0.03,
            "PRESENTATION_SELECTOR": 0.02,
            "ZWJ_SEQUENCE": 0.05,
            "REGIONAL_FLAG": 0.01,
            "COMPLEX": 0.04,
        }.get(structure_type, 0.0)

        y -= int(temp_size * y_lift)
        x = max(x, 0)
        y = max(y, 0)

        log(f"Computed render position: x={x}px, y={y}px, structure={structure_type}.", log_entries, quiet=quiet, level="DEBUG")
        return (x, y)

    except Exception as err:
        log(f"Using fallback render position after position calculation failed: {err}", log_entries, quiet=quiet, level="WARNING")
        return (temp_size // 4, temp_size // 4)
