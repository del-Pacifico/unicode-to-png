#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#
"""
Summary:
Unicode to PNG Generator is a cross-compatible Python tool for generating
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
import os
from datetime import datetime
import argparse
import textwrap

from unicode_to_png import (
    classify_unicode_structure,
    configure_console_output,
    console_message,
    get_adjusted_margin,
    get_adjusted_position,
    is_emoji,
    log,
    parse_batch,
    prepare_log_path,
    read_version,
    safe_print,
    sanitize_folder_name,
    write_log_if_needed,
)

# Enforce the minimum supported Python version before running the CLI.
if sys.version_info < (3, 10):
    sys.exit("[utp] - ERROR - Python 3.10 or higher is required.")

Image = None
ImageDraw = None
ImageFont = None
UnidentifiedImageError = None
PIL = None

# psutil is optional and only required for memory limit enforcement.
HAS_PSUTIL = False
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    pass

def ensure_runtime_dependencies():
    """Ensure runtime dependencies are installed without modifying the environment."""
    global Image, ImageDraw, ImageFont, UnidentifiedImageError, PIL
    try:
        from PIL import Image as PilImage
        from PIL import ImageDraw as PilImageDraw
        from PIL import ImageFont as PilImageFont
        from PIL import UnidentifiedImageError as PilUnidentifiedImageError
        import PIL as PilModule
    except ImportError:
        safe_print(console_message("ERROR", "Pillow is required but is not installed."))
        safe_print(console_message("INFO", "Install dependencies with: pip install -r requirements.txt"))
        return False

    pillow_version = tuple(map(int, PilModule.__version__.split('.')[:2]))
    if pillow_version < (12, 2):
        safe_print(console_message("ERROR", f"Pillow 12.2.0 or higher is required. Current version: {PilModule.__version__}"))
        return False

    Image = PilImage
    ImageDraw = PilImageDraw
    ImageFont = PilImageFont
    UnidentifiedImageError = PilUnidentifiedImageError
    PIL = PilModule
    return True

# Configure CLI argument parsing.
HELP_EPILOG = """
Usage rules:
  - Provide either --emoji or --batch.
  - Provide --folder for every generation run.
  - When --emoji and --batch are both provided, --batch is used and --emoji is ignored.
  - Use --filename-prefix or --filename-prefix-from-folder to customize output file names.
  - The CLI never asks for keyboard input. Missing required values return an error.
  - Windows is required for supported color emoji rendering.

Examples:
  Basic:
    python unicode_to_png.py --emoji "<emoji>" --folder target_icon

  Medium:
    python unicode_to_png.py --batch "<emoji>:fire,<emoji>:game" --folder browser_icons --filename-prefix-from-folder

  Advanced:
    python unicode_to_png.py --batch "<emoji>:developer,<emoji>:firefighter" --folder heroes --filename-prefix hero --quiet --autofixmargin

Output:
  - PNG icons are written to emojis/<folder>/<prefix>_<size>x<size>.png.
  - Runtime logs are written to log/YYYYMMDD_<folder>.log when warnings, errors, or operational events are recorded.

More examples:
  python unicode_to_png.py --examples
"""

EXAMPLES_TEXT = """
Unicode to PNG CLI examples

Basic single emoji:
  python unicode_to_png.py --emoji "<emoji>" --folder target_icon
  Output: emojis/target_icon/emoji_16x16.png ... emoji_128x128.png

Medium batch generation:
  python unicode_to_png.py --batch "<emoji>:fire,<emoji>:game,<emoji>:idea" --folder browser_icons
  Output:
    emojis/browser_icons_fire/emoji_*.png
    emojis/browser_icons_game/emoji_*.png
    emojis/browser_icons_idea/emoji_*.png

Automation with quiet console:
  python unicode_to_png.py --batch "<emoji>:package,<emoji>:rocket" --folder release_assets --quiet
  Console output is suppressed. Runtime events are still written to log files when collected.

Manual margin control:
  python unicode_to_png.py --emoji "<emoji>" --folder centered_icon --margin 0.2
  Use this when a fixed visual margin is required.

Custom filename prefix:
  python unicode_to_png.py --emoji "<emoji>" --folder gaming_icon --filename-prefix chrome_icon
  Output: emojis/gaming_icon/chrome_icon_16x16.png ... chrome_icon_128x128.png

Folder-based filename prefix:
  python unicode_to_png.py --batch "<emoji>:fire,<emoji>:game" --folder browser_icons --filename-prefix-from-folder
  Output:
    emojis/browser_icons_fire/browser_icons_fire_*.png
    emojis/browser_icons_game/browser_icons_game_*.png

Automatic edge correction:
  python unicode_to_png.py --emoji "<emoji>" --folder astronaut --autofixmargin
  Enables edge detection and retries rendering with increased margin when needed.

Memory monitoring:
  python unicode_to_png.py --batch "<emoji>:brain,<emoji>:science" --folder edu_pack --memlimit 500
  Requires psutil. If psutil is missing, the CLI logs a warning and continues without memory monitoring.

Mixed input rule:
  python unicode_to_png.py --emoji "<emoji>" --batch "<emoji>:fire" --folder icons
  --batch takes priority and --emoji is ignored with a warning.

Invalid usage examples:
  python unicode_to_png.py
  Error: No emoji input was provided. Use --emoji or --batch.

  python unicode_to_png.py --emoji "<emoji>"
  Error: No output folder name was provided. Use --folder.

Detailed usage document:
  docs/USAGE.md
"""


def build_help_text(text):
    return textwrap.dedent(text).strip()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate browser extension PNG icons from emoji input using explicit CLI arguments.",
        epilog=build_help_text(HELP_EPILOG),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--emoji", type=str, help="Emoji to generate.", required=False)
    parser.add_argument("--folder", type=str, help="Folder name to save icons", required=False)
    parser.add_argument("--batch", type=str, help="Comma-separated list of emojis to process", required=False)
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    parser.add_argument("--memlimit", type=int, help="Maximum memory usage (in MB) before aborting", required=False)
    parser.add_argument("--margin", type=float, help="Extra margin ratio (0.0 - 1.0) to prevent emoji clipping (default: 0.25)", required=False)
    parser.add_argument("--edgecheck", action="store_true", help="Enable visual edge test to detect emoji touching final image borders.")
    parser.add_argument("--autofixmargin", action="store_true", help="Enable edge check and re-render with increased margin if the emoji touches an edge.")
    parser.add_argument("--filename-prefix", type=str, help="Custom output filename prefix. Default: emoji.", required=False)
    parser.add_argument("--filename-prefix-from-folder", action="store_true", help="Use the sanitized output folder name as the output filename prefix.")
    parser.add_argument("--examples", action="store_true", help="Show detailed CLI examples and exit.")
    parser.add_argument("--version", action="version", version=f"unicode_to_png {read_version()}")
    return parser.parse_args()

# Return memory usage in MB for the current process when psutil is available.
def get_memory_usage_mb():
    if not HAS_PSUTIL:
        return None
    try:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
    except Exception:
        return None

# Load the Segoe UI Emoji font or fall back to the default font.
def load_font(size, quiet=False):
    font_path = "C:/Windows/Fonts/seguiemj.ttf"
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except OSError as e:
            if not quiet:
                safe_print(console_message("WARNING", f"Segoe UI Emoji could not be loaded. Reason: {e}"))
        except UnidentifiedImageError as e:
            if not quiet:
                safe_print(console_message("WARNING", f"Segoe UI Emoji font format was not recognized. Reason: {e}"))
    if not quiet:
        safe_print(console_message("WARNING", "Emoji font was not found or could not be loaded. Default font will be used."))
    return ImageFont.load_default()
    
# Detect if emoji rendering touches the right or bottom edge of the final PNG.
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
            log(f"Emoji touches {', '.join(edge_info)} edge(s) at {size_label}x{size_label}.", log_entries, quiet=quiet, level="WARNING")
    except Exception as edge_check_error:
        log(f"Visual edge test failed for {size_label}x{size_label}.", log_entries, quiet=quiet, level="WARNING", detail=str(edge_check_error))

def iter_image_pixels(image):
    """Return an iterator over image pixels while supporting newer Pillow APIs."""
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()

def main():
    configure_console_output()
    args = parse_args()
    quiet_mode = args.quiet
    startup_warnings = []

    if args.examples:
        safe_print(build_help_text(EXAMPLES_TEXT))
        sys.exit(0)

    if platform.system() != "Windows":
        safe_print(console_message("ERROR", "This script requires Windows for supported color emoji rendering."))
        sys.exit(1)

    if not ensure_runtime_dependencies():
        sys.exit(1)

    if not quiet_mode:
        safe_print(console_message("INFO", f"Unicode to PNG Generator v{read_version()} started."))
        safe_print(console_message("INFO", "Use --help to list available options and examples."))
    
    # Use a default margin ratio to reduce clipping risk.
    DEFAULT_MARGIN_RATIO = 0.25
    margin_ratio = args.margin if args.margin and args.margin > 0 else DEFAULT_MARGIN_RATIO

    if args.margin is not None and args.margin <= 0:
        startup_warnings.append(f"Invalid margin value '{args.margin}' was provided. Default margin ratio {DEFAULT_MARGIN_RATIO} will be used.")

    # Inform the user when the margin was customized.
    if args.margin and not quiet_mode:
        safe_print(console_message("INFO", f"Using custom margin ratio: {margin_ratio}."))
    
    
    # Set the memory limit used when optional memory monitoring is available.
    DEFAULT_MEMORY_LIMIT_MB = 500
    memory_limit_mb = args.memlimit if args.memlimit and args.memlimit > 0 else DEFAULT_MEMORY_LIMIT_MB
    if args.memlimit is not None and args.memlimit <= 0:
        startup_warnings.append(f"Invalid memory limit '{args.memlimit}' was provided. Default memory limit {DEFAULT_MEMORY_LIMIT_MB} MB will be used.")

    # Report memory monitoring status only when the user requested memory enforcement.
    if HAS_PSUTIL:
        if args.memlimit and not quiet_mode:
            safe_print(console_message("INFO", f"Memory limit set to {memory_limit_mb} MB."))
    else:
        if args.memlimit:
            warning = "psutil is not installed. Memory monitoring is disabled for this run."
            startup_warnings.append(warning)
            if not quiet_mode:
                safe_print(console_message("WARNING", warning))
                safe_print(console_message("INFO", "Install psutil to enable --memlimit: pip install psutil"))

    # Determine emoji + alias pairs from explicit CLI arguments only.
    if args.batch:
        if args.emoji:
            startup_warnings.append("--emoji was ignored because --batch was provided.")
        emoji_pairs, batch_warnings = parse_batch(args.batch)
        startup_warnings.extend(batch_warnings)
    else:
        if not args.emoji:
            safe_print(console_message("ERROR", "No emoji input was provided. Use --emoji or --batch."))
            sys.exit(1)

        emoji_input = args.emoji.strip()

        # Validate that the input is a printable emoji character.
        if not emoji_input or not emoji_input.isprintable() or not is_emoji(emoji_input):
            safe_print(console_message("ERROR", f"Invalid emoji input: '{emoji_input}'."))
            sys.exit(1)

        emoji_pairs = [(emoji_input, "single")]

    if not emoji_pairs:
        safe_print(console_message("ERROR", "No valid emoji entries were provided."))
        sys.exit(1)

    # Get folder name from explicit CLI arguments only.
    if not args.folder:
        safe_print(console_message("ERROR", "No output folder name was provided. Use --folder."))
        sys.exit(1)

    folder_raw = args.folder.strip()

    if not folder_raw:
        safe_print(console_message("ERROR", "No output folder name was provided."))
        sys.exit(1)
    
    enable_edge_check = args.edgecheck or args.autofixmargin
    enable_autofix_margin = args.autofixmargin

    # Clean the base folder name.
    folder_base = sanitize_folder_name(folder_raw)
    if not folder_base:
        safe_print(console_message("ERROR", f"Output folder name '{folder_raw}' is empty after sanitization."))
        sys.exit(1)
    if folder_base != folder_raw:
        startup_warnings.append(f"Output folder name was sanitized from '{folder_raw}' to '{folder_base}'.")

    if args.filename_prefix and args.filename_prefix_from_folder:
        safe_print(console_message("ERROR", "Use either --filename-prefix or --filename-prefix-from-folder, not both."))
        sys.exit(1)

    filename_prefix = "emoji"
    if args.filename_prefix:
        filename_prefix = sanitize_folder_name(args.filename_prefix.strip())
        if not filename_prefix:
            safe_print(console_message("ERROR", f"Filename prefix '{args.filename_prefix}' is empty after sanitization."))
            sys.exit(1)
        if filename_prefix != args.filename_prefix.strip():
            startup_warnings.append(f"Filename prefix was sanitized from '{args.filename_prefix}' to '{filename_prefix}'.")

    base_path = os.path.dirname(os.path.abspath(__file__))
    emojis_root = os.path.join(base_path, "emojis")
    try:
        os.makedirs(emojis_root, exist_ok=True)
    except OSError as root_error:
        safe_print(console_message("ERROR", f"Failed to prepare output root directory: {emojis_root}."))
        safe_print(console_message("ERROR", f"Output root error detail: {root_error}"))
        sys.exit(1)

    # Process each emoji and alias pair.
    for index, (emoji, alias) in enumerate(emoji_pairs, start=1):
        # Generate folder name based on CLI --folder when not in batch mode.
        subfolder_name = f"{folder_base}" if alias == "single" else f"{folder_base}_{alias}"
        active_filename_prefix = subfolder_name if args.filename_prefix_from_folder else filename_prefix
        output_path = os.path.join(emojis_root, subfolder_name)
        try:
            os.makedirs(output_path, exist_ok=True)
        except OSError as output_error:
            safe_print(console_message("WARNING", f"Output folder could not be prepared and will be skipped: {output_path}"))
            safe_print(console_message("WARNING", f"Output folder error detail: {output_error}"))
            continue


        if not os.access(output_path, os.W_OK):
            safe_print(console_message("WARNING", f"Output folder is not writable and will be skipped: {output_path}"))
            continue

        log_file = prepare_log_path(base_path, subfolder_name)
        log_entries = []

        for warning in startup_warnings:
            log(warning, log_entries, quiet=quiet_mode, level="WARNING")

        log(f"Starting PNG generation for emoji {index} into '{output_path}'.", log_entries, quiet=quiet_mode)
        log(f"Output filename prefix applied: {active_filename_prefix}.", log_entries, quiet=quiet_mode, level="DEBUG")
        log(f"Margin ratio applied: {margin_ratio}.", log_entries, quiet=quiet_mode, level="DEBUG")

        ICON_SIZES = [16, 19, 32, 38, 48, 128]
        SCALE_FACTOR = 4

        for size in ICON_SIZES:
            temp_size = size * SCALE_FACTOR
            img = Image.new("RGBA", (temp_size, temp_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Classify emoji before rendering.
            try:
                structure_type = classify_unicode_structure(emoji)
                log(f"Detected Unicode structure: {structure_type}.", log_entries, quiet=quiet_mode, level="DEBUG")
            except Exception as classify_error:
                structure_type = "COMPLEX"
                log("Emoji structure classification failed. Fallback structure COMPLEX will be used.", log_entries, quiet=quiet_mode, level="WARNING", detail=str(classify_error))

            # Load font and compute bounding box with fit checks.
            font_size = int(temp_size * 0.85)
            max_attempts = 10

            for attempt in range(max_attempts):
                font = load_font(font_size, quiet_mode)
                try:
                    bbox = draw.textbbox((0, 0), emoji, font=font, embedded_color=True)
                except TypeError:
                    bbox = draw.textbbox((0, 0), emoji, font=font)

                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]

                if width <= int(temp_size * 0.97) and height <= int(temp_size * 0.97):
                    break

                font_size -= 2

            else:
                log(f"Emoji did not fit within {temp_size}px after {max_attempts} attempts. Rendering may be clipped.", log_entries, quiet=quiet_mode, level="WARNING")

            # Validate the final bounding box before rendering.
            if not bbox or len(bbox) != 4:
                log(f"Invalid bounding box detected after fit attempts. Size {size}px will be skipped.", log_entries, quiet=quiet_mode, level="ERROR")
                continue


            # Compute structure-aware render position.
            x, y = get_adjusted_position(structure_type, temp_size, bbox, log_entries, quiet_mode)

            # Render the emoji.
            try:
                draw.text((x, y), emoji, font=font, embedded_color=True)
            except TypeError:
                draw.text((x, y), emoji, font=font)

            if all(pixel[3] == 0 for pixel in iter_image_pixels(img)):
                log(f"Emoji may not have rendered at {size}x{size}.", log_entries, quiet=quiet_mode, level="WARNING")

            # Compute structure-aware margin.
            try:
                margin_pixels = get_adjusted_margin(structure_type, margin_ratio, temp_size)
                log(f"Adjusted margin: {margin_pixels}px for structure {structure_type}.", log_entries, quiet=quiet_mode, level="DEBUG")
            except Exception as margin_error:
                margin_pixels = int(temp_size * margin_ratio)
                log(f"Margin adaptation failed. Base margin {margin_pixels}px will be used.", log_entries, quiet=quiet_mode, level="WARNING", detail=str(margin_error))

            # Crop and resize with optional retry when an edge is touched.
            def render_with_margin_and_test(img, temp_size, bbox, size, margin_px, enable_check, log_entries, quiet, x, y):
                crop_left = max(x - margin_px, 0)
                crop_top = max(y - margin_px, 0)
                crop_right = min(x + (bbox[2] - bbox[0]) + margin_px, temp_size)
                crop_bottom = min(y + (bbox[3] - bbox[1]) + margin_px, temp_size)

                cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
                resized = cropped.resize((size, size), Image.LANCZOS)

                # Check visual borders when edge checking is enabled.
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
                            log(f"Emoji touches {', '.join(edge_info)} edge(s) at {size}x{size}.", log_entries, quiet=quiet, level="WARNING")
                            return resized, True
                    except Exception as edge_error:
                        log(f"Visual edge test failed at {size}x{size}.", log_entries, quiet=quiet, level="WARNING", detail=str(edge_error))

                return resized, False

            try:
                resized_img, needs_retry = render_with_margin_and_test(
                    img, temp_size, bbox, size, margin_pixels, enable_edge_check, log_entries, quiet_mode, x, y
                )

                # Retry with increased margin when autofix is enabled.
                if needs_retry and enable_autofix_margin:
                    retry_margin = int(margin_pixels * 1.4)
                    log(f"Re-rendering with increased margin: {retry_margin}px.", log_entries, quiet=quiet_mode)
                    resized_img, _ = render_with_margin_and_test(
                        img, temp_size, bbox, size, retry_margin, False, log_entries, quiet_mode, x, y
                    )

            except Exception as crop_error:
                log(f"Cropping or resizing failed for {size}x{size}. Size will be skipped.", log_entries, quiet=quiet_mode, level="ERROR", detail=str(crop_error))
                continue



            filename = f"{active_filename_prefix}_{size}x{size}.png"
            file_path = os.path.join(output_path, filename)

            # Enforce memory usage limit when optional monitoring is available.
            memory_mb = get_memory_usage_mb()
            if memory_mb:
                if memory_mb > memory_limit_mb:
                    log(f"Memory usage exceeded configured limit: {memory_mb:.1f} MB > {memory_limit_mb} MB.", log_entries, quiet=quiet_mode, level="ERROR")
                    write_log_if_needed(log_entries, log_file)
                    safe_print(console_message("ERROR", f"Process aborted due to excessive memory usage: {memory_mb:.1f} MB."))
                    sys.exit(1)
                elif memory_mb > 300:
                    log(f"Memory usage is high: {memory_mb:.1f} MB.", log_entries, quiet=quiet_mode, level="WARNING")

            if os.path.exists(file_path):
                log(f"Existing output file will be overwritten: {filename}.", log_entries, quiet=quiet_mode, level="WARNING")

            try:
                resized_img.save(file_path)
                log(f"Icon generated: {filename}.", log_entries, quiet=quiet_mode)
            except (OSError, IOError) as e:
                log(f"Failed to save output file: {filename}.", log_entries, quiet=quiet_mode, level="ERROR", detail=str(e))
                continue
            finally:
                # Release image objects before processing the next output size.
                try:
                    del draw, resized_img, img
                except NameError:
                    pass

        log(f"Completed PNG generation for emoji {index} into '{output_path}'.", log_entries, quiet=quiet_mode)
        write_log_if_needed(log_entries, log_file)


# Entry point when the script is executed directly.
if __name__ == "__main__":
    import traceback

    try:
        main()
    except Exception as e:
        # Write detailed diagnostics to the fallback log while keeping console output concise.
        error_trace = traceback.format_exc()
        console_error = "Unexpected error occurred. See the fallback error log for details."
        safe_print(console_message("ERROR", console_error))

        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(base_path, "log")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, datetime.now().strftime("%Y%m%d") + "_error.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {console_error}\n")
                f.write(f"{error_trace}\n")
        except Exception as log_error:
            safe_print(console_message("ERROR", f"Failed to write fallback error log: {log_error}"))

        sys.exit(1)


