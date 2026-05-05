#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""Filesystem path helpers for Unicode to PNG."""

from datetime import datetime
import os
import re


def sanitize_folder_name(name):
    """Remove characters from a folder name unless they are alphanumeric or underscores."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", name).strip("_")


def prepare_log_path(base_dir, folder_name):
    """Prepare the full path to the log file and ensure the log directory exists."""
    log_dir = os.path.join(base_dir, "log")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError:
        return None

    date_str = datetime.now().strftime("%Y%m%d")
    log_filename = f"{date_str}_{folder_name}.log"
    return os.path.join(log_dir, log_filename)
