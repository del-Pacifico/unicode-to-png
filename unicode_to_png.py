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
📌 Summary:
Unicode to PNG Generator v1.19 is a cross-compatible Python tool for generating
browser extension icon sets (16px–128px) from emoji symbols. It supports complex
emoji structures (e.g. skin modifiers, ZWJ sequences, flags), with smart centering,
adaptive font fitting, and optional edge-aware margin correction.

Icons are saved in organized subfolders under /emojis, and logs are created only if
warnings or errors occur. Built-in options include memory limits, visual edge checks,
and automated retry with increased margins.

Perfect for developers needing quick, precise, and visually safe emoji-based icons
for web and extension projects.
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

# ✅ Optional: Import psutil if available for memory monitoring
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# 🧩 Setup CLI argument parsing
def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate browser extension icons from a single emoji or emoji batch."
    )
    parser.add_argument("--emoji", type=str, help="Emoji to generate (e.g. 🖼️)", required=False)
    parser.add_argument("--folder", type=str, help="Folder name to save icons", required=False)
    parser.add_argument("--batch", type=str, help="Comma-separated list of emojis to process", required=False)
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    parser.add_argument("--memlimit", type=int, help="Maximum memory usage (in MB) before aborting", required=False)
    parser.add_argument("--margin", type=float, help="Extra margin ratio (0.0 - 1.0) to prevent emoji clipping (default: 0.25)", required=False)
    parser.add_argument("--edgecheck", action="store_true", help="Enable visual edge test to detect emoji touching final image borders.")
    parser.add_argument("--autofixmargin", action="store_true", help="If edge is touched, re-render with increased margin (only applies if --edgecheck is active).")
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
    
# 🧠 Classifies the emoji based on its Unicode structure
def classify_unicode_structure(emoji: str) -> str:
    """
    Classifies the emoji into structural categories:
    SIMPLE, SKIN_MODIFIER, PRESENTATION_SELECTOR, ZWJ_SEQUENCE, REGIONAL_FLAG, COMPLEX.

    Args:
        emoji (str): The emoji character string.

    Returns:
        str: Classification category.
    """
    try:
        codepoints = [ord(c) for c in emoji]

        # 👨‍👩‍👧‍👦 → ZWJ-based sequence
        if 0x200D in codepoints:
            return "ZWJ_SEQUENCE"

        # ✍🏻 → base + tone modifier (U+1F3FB - U+1F3FF)
        if any(0x1F3FB <= cp <= 0x1F3FF for cp in codepoints):
            return "SKIN_MODIFIER"

        # ✏️ → emoji + U+FE0F presentation selector
        if 0xFE0F in codepoints:
            return "PRESENTATION_SELECTOR"

        # 🇨🇱 → regional indicators (flags)
        if all(0x1F1E6 <= cp <= 0x1F1FF for cp in codepoints):
            return "REGIONAL_FLAG"

        # 🧱 → monolithic
        if len(codepoints) == 1:
            return "SIMPLE"

        # Any unrecognized structure
        return "COMPLEX"

    except Exception as err:
        return "COMPLEX"
        
# 📏 Computes final margin based on structure type
def get_adjusted_margin(structure_type, base_ratio, size_px):
    """
    Calculates a structure-aware margin in pixels.

    Args:
        structure_type (str): Classification from classify_unicode_structure(...)
        base_ratio (float): User-defined or default margin ratio
        size_px (int): Canvas size in pixels

    Returns:
        int: Total margin in pixels
    """
    boost = {
        "SKIN_MODIFIER": 0.10,
        "PRESENTATION_SELECTOR": 0.08,
        "ZWJ_SEQUENCE": 0.12,
        "REGIONAL_FLAG": 0.06,
        "COMPLEX": 0.15
    }.get(structure_type, 0.0)

    total_ratio = base_ratio + boost
    return int(size_px * total_ratio)

# 🎯 Computes final (x, y) render position with vertical compensation
def get_adjusted_position(structure_type, temp_size, bbox, log_entries, quiet):
    """
    Returns corrected (x, y) coordinates for drawing emoji, compensating for Unicode type.

    Args:
        structure_type (str): Classification from classify_unicode_structure(...)
        temp_size (int): Base canvas size
        bbox (tuple): Bounding box from draw.textbbox()
        log_entries (list): Log collection
        quiet (bool): Suppress console output

    Returns:
        tuple: (x, y) coordinates
    """
    try:
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        x = (temp_size - width) // 2 - bbox[0]
        y = (temp_size - height) // 2 - bbox[1]

        # Adjustment map
        y_lift = {
            "SKIN_MODIFIER": 0.03,
            "PRESENTATION_SELECTOR": 0.02,
            "ZWJ_SEQUENCE": 0.05,
            "REGIONAL_FLAG": 0.01,
            "COMPLEX": 0.04
        }.get(structure_type, 0.0)

        y -= int(temp_size * y_lift)
        x = max(x, 0)
        y = max(y, 0)

        log(f"📐 Center position: x={x}px, y={y}px for type '{structure_type}'", log_entries, quiet=quiet)
        return (x, y)

    except Exception as err:
        log(f"[!] Fallback position due to error: {err}", log_entries, quiet=quiet)
        return (temp_size // 4, temp_size // 4)

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
            
# 🔎 Returns memory usage in MB of the current process if psutil is available
def get_memory_usage_mb():
    if not HAS_PSUTIL:
        return None
    try:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    except Exception:
        return None

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
    
# 🧪 Optional test: Detect if emoji rendering touches right or bottom edge of final PNG
def check_visual_edges(image, size_label, log_entries, quiet):
    """
    Checks if any opaque pixel touches the right or bottom edge of the image.
    Logs a warning if detected.

    Args:
        image (PIL.Image): Final resized emoji image
        size_label (int): Output size label (e.g. 128)
        log_entries (list): Log collector
        quiet (bool): Suppress console output
    """
    try:
        pixels = image.load()
        width, height = image.size

        touches_right = any(pixels[width - 1, y][3] != 0 for y in range(height))
        touches_bottom = any(pixels[x, height - 1][3] != 0 for x in range(width))

        if touches_right or touches_bottom:
            edge_info = []
            if touches_right:
                edge_info.append("right")
            if touches_bottom:
                edge_info.append("bottom")
            log(f"[!] Visual edge warning: emoji touches {', '.join(edge_info)} edge(s) at {size_label}x{size_label}", log_entries, quiet=quiet)
            log(f" ", log_entries, quiet=quiet)
    except Exception as edge_check_error:
        log(f"[!] Visual edge test failed: {edge_check_error}", log_entries, quiet=quiet)

def main():
    print("""
🖼️ Unicode to PNG Generator v1.19
---------------------------------------------
Generate a complete set of browser extension icons (16px to 128px) from any emoji,
now with structure-aware centering, adaptive font fitting, and edge-aware margin control.

✅ Supports:
- Single emojis (monolithic)
- Emojis with skin tone modifiers (e.g. ✍🏻)
- Emojis using presentation selectors (e.g. ✏️)
- Composite ZWJ sequences (e.g. 👨‍💻, 🧑‍🚒)
- Regional flags and fallback complex cases

📦 Requirements:
- Python 3.6+
- Pillow ≥ 9.0 (install via: pip install pillow)
- Windows OS with Segoe UI Emoji font installed

🧠 Optional Enhancements:
- Memory monitoring with psutil (for --memlimit support)
  → pip install psutil

📌 Usage Examples:

# 🔹 Simple emoji (monolithic)
python unicode_to_png.py --emoji "🧱" --folder bricks
python unicode_to_png.py --emoji "🧼" --folder hygiene --margin 0.2

# 🔸 Emoji with skin tone or modifiers
python unicode_to_png.py --emoji "✍🏻" --folder handwriting
python unicode_to_png.py --emoji "👍🏽" --folder thumbs --margin 0.3

# 🔻 Composite or ZWJ emojis
python unicode_to_png.py --emoji "👨‍💻" --folder coder
python unicode_to_png.py --emoji "🧑‍🚒" --folder firefighter --margin 0.35

# 🔀 Batch mode with aliases
python unicode_to_png.py --batch "📦:box,🎮:game" --folder myicons
python unicode_to_png.py --batch "💡:idea,👨‍🚀:astro" --folder assets --margin 0.25 --edgecheck --autofixmargin

⚙️ Optional Parameters:
--memlimit       : Abort if memory usage exceeds this value (in MB).
--margin         : Extra margin ratio (default: 0.25). Applies adaptive boost based on emoji structure.
--edgecheck      : Run visual test to detect if emoji touches final image borders (right or bottom).
--autofixmargin  : If edge is touched, re-render image with increased margin (requires --edgecheck).
--quiet          : Suppress console output (logs are still generated if needed).

📁 Output:
- PNG icons saved under 'emojis/<folder>/' directory
- Log file written to 'log/YYYYMMDD_<folder>.log' if any warning or error occurs
""")


    args = parse_args()
    
    # ✏️ Default margin ratio to prevent cropping
    DEFAULT_MARGIN_RATIO = 0.25
    margin_ratio = args.margin if args.margin and args.margin > 0 else DEFAULT_MARGIN_RATIO

    # 🔔 Inform user if margin was customized
    if args.margin:
        print(f"[i] Using custom margin ratio: {margin_ratio}")
    
    
    # 🧠 Set dynamic memory limit for abortion
    DEFAULT_MEMORY_LIMIT_MB = 500
    memory_limit_mb = args.memlimit if args.memlimit and args.memlimit > 0 else DEFAULT_MEMORY_LIMIT_MB

    # 🧠 Inform user only if memory monitoring is active and the limit will actually be used
    if HAS_PSUTIL:
        if args.memlimit:
            print(f"[i] Memory limit set to {memory_limit_mb} MB")
    else:
        print("[i] psutil module not found. Memory monitoring and --memlimit are disabled.")
        print("[i] To enable memory monitoring, run: pip install psutil")

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
    
    enable_edge_check = args.edgecheck
    enable_autofix_margin = args.autofixmargin

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
        log(f"🧮 Margin ratio applied: {margin_ratio}", log_entries, quiet=quiet_mode)

        ICON_SIZES = [16, 19, 32, 38, 48, 128]
        SCALE_FACTOR = 4

        for size in ICON_SIZES:
            temp_size = size * SCALE_FACTOR
            img = Image.new("RGBA", (temp_size, temp_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 🔍 Step 0: Classify emoji before rendering
            try:
                structure_type = classify_unicode_structure(emoji)
                log(f"🔍 Unicode structure detected: {structure_type}", log_entries, quiet=quiet_mode)
            except Exception as classify_error:
                structure_type = "COMPLEX"
                log(f"[!] Failed to classify emoji structure: {classify_error}", log_entries, quiet=quiet_mode)

            # 🔁 Step 1: Load font and compute bounding box with fit check
            font_size = int(temp_size * 0.85)  # Start more conservatively (e.g. 85% of canvas)
            max_attempts = 10

            for attempt in range(max_attempts):
                font = load_font(font_size)
                try:
                    bbox = draw.textbbox((0, 0), emoji, font=font, embedded_color=True)
                except TypeError:
                    bbox = draw.textbbox((0, 0), emoji, font=font)

                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]

                if width <= int(temp_size * 0.97) and height <= int(temp_size * 0.97):
                    break  # ✅ Emoji fits, safe to proceed

                font_size -= 2  # 🔁 Reduce font size to try again

            else:
                log(f"[!] Emoji could not fit within {temp_size}px after {max_attempts} attempts. Rendering may be clipped.", log_entries, quiet=quiet_mode)

            # Final validation of bbox
            if not bbox or len(bbox) != 4:
                log(f"[✗] Invalid bounding box detected after fit attempts. Skipping size {size}px.", log_entries, quiet=quiet_mode)
                continue


            # 🎯 Step 2: Compute structure-aware position via utility
            x, y = get_adjusted_position(structure_type, temp_size, bbox, log_entries, quiet_mode)

            # ✍️ Step 3: Render emoji
            try:
                draw.text((x, y), emoji, font=font, embedded_color=True)
            except TypeError:
                draw.text((x, y), emoji, font=font)

            if all(pixel[3] == 0 for pixel in img.getdata()):
                log(f"[!] Warning: Emoji may not have rendered at {size}x{size}", log_entries, quiet=quiet_mode)

            # 📏 Step 4: Compute structure-aware margin via utility
            try:
                margin_pixels = get_adjusted_margin(structure_type, margin_ratio, temp_size)
                log(f"🎯 Adjusted margin: {margin_pixels}px for type '{structure_type}'", log_entries, quiet=quiet_mode)
            except Exception as margin_error:
                margin_pixels = int(temp_size * margin_ratio)
                log(f"[!] Failed margin adaptation: {margin_error}. Using base margin: {margin_pixels}px", log_entries, quiet=quiet_mode)

            # ✂️ Step 5: Crop and resize with optional retry if edge is touched
            def render_with_margin_and_test(img, temp_size, bbox, size, margin_px, enable_check, log_entries, quiet, x, y):
                crop_left = max(x - margin_px, 0)
                crop_top = max(y - margin_px, 0)
                crop_right = min(x + (bbox[2] - bbox[0]) + margin_px, temp_size)
                crop_bottom = min(y + (bbox[3] - bbox[1]) + margin_px, temp_size)

                cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
                resized = cropped.resize((size, size), Image.LANCZOS)

                # 🧪 Check visual borders
                if enable_check:
                    try:
                        pixels = resized.load()
                        width, height = resized.size
                        touches_right = any(pixels[width - 1, y][3] != 0 for y in range(height))
                        touches_bottom = any(pixels[x, height - 1][3] != 0 for x in range(width))
                        if touches_right or touches_bottom:
                            edge_info = []
                            if touches_right: edge_info.append("right")
                            if touches_bottom: edge_info.append("bottom")
                            log(f"[!] Visual edge warning: emoji touches {', '.join(edge_info)} edge(s) at {size}x{size}", log_entries, quiet=quiet)
                            log(f" ", log_entries, quiet=quiet)
                            return resized, True
                    except Exception as edge_error:
                        log(f"[!] Visual edge test failed: {edge_error}", log_entries, quiet=quiet)

                return resized, False

            try:
                resized_img, needs_retry = render_with_margin_and_test(
                    img, temp_size, bbox, size, margin_pixels, enable_edge_check, log_entries, quiet_mode, x, y
                )

                # 🔁 Step 5b: Retry with increased margin
                if needs_retry and enable_autofix_margin:
                    retry_margin = int(margin_pixels * 1.4)
                    log(f"[i] Re-rendering with increased margin: {retry_margin}px", log_entries, quiet=quiet_mode)
                    resized_img, _ = render_with_margin_and_test(
                        img, temp_size, bbox, size, retry_margin, False, log_entries, quiet_mode, x, y
                    )

            except Exception as crop_error:
                log(f"[✗] Failed during cropping/resizing: {crop_error}", log_entries, quiet=quiet_mode)
                continue



            filename = f"emoji_{size}x{size}.png"
            file_path = os.path.join(output_path, filename)

            # 🧠 Step 6: Memory usage control
            memory_mb = get_memory_usage_mb()
            if memory_mb:
                if memory_mb > memory_limit_mb:
                    log(f"[✗] Aborting: Memory usage exceeded safe limit ({memory_mb:.1f} MB > {memory_limit_mb} MB)", log_entries, quiet=quiet_mode)
                    write_log_if_needed(log_entries, log_file)
                    print(f"[✗] Process aborted due to excessive memory usage: {memory_mb:.1f} MB")
                    sys.exit(1)
                elif memory_mb > 300:
                    log(f"[!] Warning: Memory usage is high ({memory_mb:.1f} MB)", log_entries, quiet=quiet_mode)

            if os.path.exists(file_path):
                log(f"[!] Overwriting existing file: {filename}", log_entries, quiet=quiet_mode)

            try:
                resized_img.save(file_path)
                log(f"[✓] Icon generated: {filename}", log_entries, quiet=quiet_mode)
            except (OSError, IOError) as e:
                log(f"[✗] Failed to save {filename}: {e}", log_entries, quiet=quiet_mode)
                continue
            finally:
                # 🔄 Step 7: Memory cleanup
                for obj in ['draw', 'resized_img', 'img']:
                    try:
                        del locals()[obj]
                    except:
                        pass


# ▶️ Entry point of the script when executed directly (not imported as a module)
if __name__ == "__main__":
    import traceback

    try:
        main()
    except Exception as e:
        # ❗ Catch any unhandled exception and log it to a fallback file with full traceback
        error_trace = traceback.format_exc()
        error_msg = f"[✗] Unexpected error occurred:\n{error_trace}"
        print(error_msg)

        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(base_path, "log")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, datetime.now().strftime("%Y%m%d") + "_error.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n{error_msg}\n")
        except Exception as log_error:
            print(f"[!] Failed to write to fallback log file: {log_error}")

        sys.exit(1)  # 🔚 Ensure the process exits with error status


