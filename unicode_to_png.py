#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/sergiopalmah/unicode_to_png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""
🖼️ Emoji Icon Generator for Browser Extensions v.1.12
---------------------------------------------

This script generates PNG icons of various standard sizes required for web browser extensions,
based on a user-provided Unicode emoji character.

✔ Input: Any emoji symbol (e.g. 🖼️, 🐱, 🔥, 🎮, 👨‍💻, 🧑‍🚒)
✔ Output: PNG icon files in the following sizes:
   - 16x16 (favicon or action icon)
   - 19x19 (toolbar icon in Chromium)
   - 32x32 (context menu support)
   - 38x38 (high DPI support)
   - 48x48 (extension page icon)
   - 128x128 (web store/public listing icon)

✔ Icons are saved in a user-defined subfolder inside the 'emojis' directory.
✔ If any error occurs, a log file is generated inside 'log/' folder with format YYYYMMDD_<emoji_name>.log

Requirements:
- Python 3.6+
- Pillow (PIL) library ≥ 9.0
- Windows OS with Segoe UI Emoji font installed (default in Windows 10+)

Supports:
- Composite emojis using ZWJ (Zero Width Joiner), such as 👨‍👩‍👧‍👦 or 🧑‍🚀
- Embedded color rendering with supported fonts
"""

import sys
import platform

# ✅ Ensure minimum Python version is 3.6
if sys.version_info < (3, 6):
    sys.exit(f"[✗] This script requires Python 3.6 or higher.")

# ✅ Warn user if not on Windows
if platform.system() != "Windows":
    sys.exit(f"[!] Warning: This script was designed for Windows and may not render emojis correctly on other systems.")

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import PIL
import os
import re
from datetime import datetime
import argparse

# 🧩 Setup CLI argument parsing
def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate browser extension icons from a single emoji or emoji batch."
    )
    parser.add_argument("--emoji", type=str, help="Emoji to generate (e.g. 🖼️)", required=False)
    parser.add_argument("--folder", type=str, help="Folder name to save icons", required=False)
    parser.add_argument("--batch", type=str, help="Comma-separated list of emojis to process", required=False)
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    return parser.parse_args()


# ✅ Ensure minimum Pillow version is 9.0
pillow_version = tuple(map(int, PIL.__version__.split('.')[:2]))
if pillow_version < (9, 0):
    sys.exit(f"[✗] Pillow 9.0+ is required. Your version is: {PIL.__version__}")

# Removes any characters from the folder name that are not alphanumeric or underscores
def sanitize_folder_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name).strip('_')
    
# ✅ Validates whether a character is an emoji using common Unicode ranges
def is_emoji(character):
    return any([
        '\U0001F300' <= character <= '\U0001F5FF',  # Misc Symbols and Pictographs
        '\U0001F600' <= character <= '\U0001F64F',  # Emoticons
        '\U0001F680' <= character <= '\U0001F6FF',  # Transport and Map Symbols
        '\U0001F700' <= character <= '\U0001F77F',  # Alchemical Symbols
        '\U0001F780' <= character <= '\U0001F7FF',  # Geometric Shapes Extended
        '\U0001F800' <= character <= '\U0001F8FF',  # Supplemental Arrows-C
        '\U0001F900' <= character <= '\U0001F9FF',  # Supplemental Symbols and Pictographs
        '\U0001FA00' <= character <= '\U0001FA6F',  # Extended-A
        '\U0001FA70' <= character <= '\U0001FAFF',  # Extended-B
        '\u2600'     <= character <= '\u26FF',      # Misc symbols
        '\u2700'     <= character <= '\u27BF',      # Dingbats
    ])

# 🔍 Parse the --batch argument into (emoji, alias) pairs
def parse_batch(batch_string):
    pairs = []
    fallback_count = 1
    for entry in batch_string.split(','):
        parts = entry.strip().split(':')
        emoji = parts[0].strip()
        if not emoji or not emoji.isprintable():
            continue  # skip invalid emoji

        # Get alias if present and sanitize it
        if len(parts) > 1 and parts[1].strip():
            alias = sanitize_folder_name(parts[1].strip())
        else:
            alias = f"emoji{fallback_count}"
            fallback_count += 1

        pairs.append((emoji, alias))
    return pairs

# Prepares the full path to the log file, ensuring 'log/' directory exists
def prepare_log_path(base_dir, folder_name):
    log_dir = os.path.join(base_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    log_filename = f"{date_str}_{folder_name}.log"
    return os.path.join(log_dir, log_filename)

# ✏️ Log message (printed to console unless in quiet mode, always recorded in log_entries)
def log(message, log_entries, quiet=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    if not quiet:
        print(line)
    log_entries.append(line)

# Writes the collected log entries to file if any are present
def write_log_if_needed(log_entries, log_file):
    if log_entries:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write('\n'.join(log_entries) + "\n")

# Loads the Segoe UI Emoji font or falls back to the default if not found
def load_font(size):
    font_path = "C:/Windows/Fonts/seguiemj.ttf"
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except OSError as e:
            print(f"[✗] Font could not be loaded (OSError): {e}")
        except UnidentifiedImageError as e:
            print(f"[✗] Unrecognized font format: {e}")
    print("[!] Emoji font not found or could not be loaded. Using default font.")
    return ImageFont.load_default()

def main():
    print("""
🖼️ Emoji Icon Generator for Browser Extensions
---------------------------------------------
Generate a full set of browser extension icons (16px to 128px) from a single emoji.
Developed for developers who need to create quick and consistent extension icons from emojis.

Requirements:
- Python 3.6+
- Pillow installed (pip install pillow)
- Windows OS with Segoe UI Emoji font
""")

    args = parse_args()

    # Determine emoji + alias pairs from --batch, --emoji, or interactive
    if args.batch:
        emoji_pairs = parse_batch(args.batch)
    else:
        emoji_input = args.emoji.strip() if args.emoji else input("🔤 Enter the emoji symbol: ").strip()

        # ✅ Validate that the input is a printable emoji character
        if not emoji_input or not emoji_input.isprintable() or not is_emoji(emoji_input):
            print(f"[✗] Invalid input: '{emoji_input}' is not a recognized emoji. Exiting.")
            sys.exit(1)

        emoji_pairs = [(emoji_input, "single")]  # ➕ avoid alias duplication in --folder mode

    # Get folder name from CLI or prompt
    if args.folder:
        folder_raw = args.folder.strip()
    else:
        folder_raw = input("📁 Folder name to save icons (e.g. emoji_spy_glass): ").strip()

    if not folder_raw:
        print(f"[✗] No folder name entered. Exiting.")
        sys.exit(1)

    quiet_mode = args.quiet

    # Clean the base folder name
    folder_base = sanitize_folder_name(folder_raw)
    base_path = os.path.dirname(os.path.abspath(__file__))
    emojis_root = os.path.join(base_path, "emojis")
    os.makedirs(emojis_root, exist_ok=True)

    # Loop through each emoji + alias pair
    for index, (emoji, alias) in enumerate(emoji_pairs, start=1):
        # ➕ Generate folder name based on CLI --folder when not in batch mode
        subfolder_name = f"{folder_base}" if alias == "single" else f"{folder_base}_{alias}"
        output_path = os.path.join(emojis_root, subfolder_name)
        os.makedirs(output_path, exist_ok=True)


        if not os.access(output_path, os.W_OK):
            print(f"[✗] Cannot write to the output folder: {output_path}")
            continue  # Try next emoji

        log_file = prepare_log_path(base_path, subfolder_name)
        log_entries = []

        log(f"🧩 Generating icon for emoji {index}: '{emoji}' → folder '{output_path}'", log_entries, quiet=quiet_mode)

        ICON_SIZES = [16, 19, 32, 38, 48, 128]
        SCALE_FACTOR = 4

        for size in ICON_SIZES:
            temp_size = size * SCALE_FACTOR
            img = Image.new("RGBA", (temp_size, temp_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            font = load_font(temp_size - 20)

            try:
                bbox = draw.textbbox((0, 0), emoji, font=font, embedded_color=True)
            except TypeError:
                bbox = draw.textbbox((0, 0), emoji, font=font)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (temp_size - text_width) // 2 - bbox[0]
            y = (temp_size - text_height) // 2 - bbox[1]

            try:
                draw.text((x, y), emoji, font=font, embedded_color=True)
            except TypeError:
                draw.text((x, y), emoji, font=font)

            if all(pixel[3] == 0 for pixel in img.getdata()):
                log(f"[!] Warning: Emoji may not have rendered at {size}x{size}", log_entries, quiet=quiet_mode)

            resized_img = img.resize((size, size), Image.LANCZOS)
            filename = f"emoji_{size}x{size}.png"
            file_path = os.path.join(output_path, filename)

            if os.path.exists(file_path):
                log(f"[!] Overwriting existing file: {filename}", log_entries, quiet=quiet_mode)

            try:
                resized_img.save(file_path)
                log(f"[✓] Icon generated: {filename}", log_entries, quiet=quiet_mode)
            except (OSError, IOError) as e:
                log(f"[✗] Failed to save {filename}: {e}", log_entries, quiet=quiet_mode)
                continue

        log("✅ Icon set completed successfully.", log_entries, quiet=quiet_mode)
        log("🚀 Folder ready for browser extension use.", log_entries, quiet=quiet_mode)
        write_log_if_needed(log_entries, log_file)

# ▶️ Entry point of the script when executed directly (not imported as a module)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # ❗ Catch any unhandled exception and log it to a fallback file
        error_msg = f"[✗] Unexpected error occurred: {e}"
        print(error_msg)

        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(base_path, "log")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, datetime.now().strftime("%Y%m%d") + "_error.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}\n")
        except Exception as log_error:
            print(f"[!] Failed to write to fallback log file: {log_error}")

        sys.exit(1)  # 🔚 Ensure the process exits with error status

