#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""Console and file logging helpers for the Unicode to PNG CLI."""

from datetime import datetime
import sys


def configure_console_output():
    """Make console output tolerant of terminals that cannot encode emoji."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass


def safe_print(message="", **kwargs):
    """Print text without crashing on legacy Windows console encodings."""
    try:
        print(message, **kwargs)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        safe_message = str(message).encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(safe_message, **kwargs)


def console_message(level, message):
    """Build a consistent console message."""
    return f"[utp] - {level.upper()} - {message}"


def log(message, log_entries, quiet=False, level="INFO", detail=None):
    """Record a log message and print it to the console unless quiet mode is enabled."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normalized_level = level.upper()
    line = f"[{timestamp}] [{normalized_level}] {message}"
    if detail:
        line = f"{line} Detail: {detail}"
    if not quiet:
        safe_print(console_message(normalized_level, message))
    log_entries.append(line)


def write_log_if_needed(log_entries, log_file):
    """Write collected log entries to file when entries exist."""
    if not log_entries:
        return True

    if not log_file:
        safe_print(console_message("WARNING", "Log file path is unavailable. Runtime log entries were not persisted."))
        return False

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n".join(log_entries) + "\n")
    except OSError as error:
        safe_print(console_message("WARNING", f"Failed to write runtime log file: {log_file}."))
        safe_print(console_message("WARNING", f"Log persistence error detail: {error}"))
        return False

    return True
