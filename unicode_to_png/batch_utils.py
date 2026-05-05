#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""Batch input parsing helpers for Unicode to PNG."""

from .path_utils import sanitize_folder_name


def parse_batch(batch_string):
    """Parse the --batch argument into emoji and alias pairs."""
    pairs = []
    warnings = []
    fallback_count = 1
    for entry_number, entry in enumerate(batch_string.split(","), start=1):
        parts = entry.strip().split(":")
        emoji = parts[0].strip()
        if not emoji or not emoji.isprintable():
            warnings.append(f"Skipped batch entry {entry_number} because the emoji value is empty or not printable.")
            continue

        # Get alias if present and sanitize it.
        if len(parts) > 1 and parts[1].strip():
            alias = sanitize_folder_name(parts[1].strip())
            if not alias:
                alias = f"emoji{fallback_count}"
                fallback_count += 1
                warnings.append(f"Batch entry {entry_number} alias was empty after sanitization. Fallback alias '{alias}' was used.")
        else:
            alias = f"emoji{fallback_count}"
            fallback_count += 1
            warnings.append(f"Batch entry {entry_number} has no alias. Fallback alias '{alias}' was used.")

        pairs.append((emoji, alias))
    return pairs, warnings
