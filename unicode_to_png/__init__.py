#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""Core helpers for the Unicode to PNG CLI."""

from .batch_utils import parse_batch
from .logging_utils import configure_console_output, console_message, log, safe_print, write_log_if_needed
from .path_utils import prepare_log_path, sanitize_folder_name
from .unicode_utils import classify_unicode_structure, get_adjusted_margin, get_adjusted_position, is_emoji
from .version import read_version

__all__ = [
    "classify_unicode_structure",
    "configure_console_output",
    "console_message",
    "get_adjusted_margin",
    "get_adjusted_position",
    "is_emoji",
    "log",
    "parse_batch",
    "prepare_log_path",
    "read_version",
    "safe_print",
    "sanitize_folder_name",
    "write_log_if_needed",
]
