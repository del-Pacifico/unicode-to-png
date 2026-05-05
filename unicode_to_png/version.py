#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""Version helpers for Unicode to PNG."""

from pathlib import Path


def read_version(root_dir=None):
    """Read the project version from the root VERSION file."""
    base_dir = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[1]
    version_file = base_dir / "VERSION"
    try:
        version = version_file.read_text(encoding="utf-8").strip()
        return version or "0.0.0"
    except OSError:
        return "0.0.0"
