# 🧙🏻‍♂️ Unicode to PNG Usage Guide

This document describes how to run the Unicode to PNG CLI with explicit arguments.
The tool does not read missing values from keyboard prompts.

## Required Arguments

Every generation run must include one input option and one output folder option.

Use one of these input options:

```powershell
python unicode_to_png.py --emoji "🎯" --folder target_icon
python unicode_to_png.py --batch "🔥:fire,🎮:game" --folder browser_icons
```

The `--folder` argument is always required for generation.

## Input Modes

### Single Emoji

```powershell
python unicode_to_png.py --emoji "🎯" --folder target_icon
```

Output:

```text
emojis/target_icon/emoji_16x16.png
emojis/target_icon/emoji_19x19.png
emojis/target_icon/emoji_32x32.png
emojis/target_icon/emoji_38x38.png
emojis/target_icon/emoji_48x48.png
emojis/target_icon/emoji_128x128.png
```

### Batch Input

```powershell
python unicode_to_png.py --batch "🔥:fire,🎮:game,💡:idea" --folder browser_icons
```

Output:

```text
emojis/browser_icons_fire/emoji_*.png
emojis/browser_icons_game/emoji_*.png
emojis/browser_icons_idea/emoji_*.png
```

If `--emoji` and `--batch` are both provided, `--batch` takes priority and `--emoji` is ignored with a warning.

## Output Filename Prefix

The default filename prefix is `emoji`.

```powershell
python unicode_to_png.py --emoji "🎯" --folder target_icon
```

Output:

```text
emojis/target_icon/emoji_16x16.png
emojis/target_icon/emoji_128x128.png
```

Use `--filename-prefix` for a custom prefix:

```powershell
python unicode_to_png.py --emoji "🎯" --folder target_icon --filename-prefix chrome_icon
```

Output:

```text
emojis/target_icon/chrome_icon_16x16.png
emojis/target_icon/chrome_icon_128x128.png
```

Use `--filename-prefix-from-folder` to derive the filename prefix from the sanitized output folder name:

```powershell
python unicode_to_png.py --batch "🔥:fire,🎮:game" --folder browser_icons --filename-prefix-from-folder
```

Output:

```text
emojis/browser_icons_fire/browser_icons_fire_16x16.png
emojis/browser_icons_game/browser_icons_game_16x16.png
```

`--filename-prefix` and `--filename-prefix-from-folder` are mutually exclusive.
If the custom prefix is empty after sanitization, the CLI exits with an objective error.

## Automation

Use `--quiet` to suppress console output during automated runs:

```powershell
python unicode_to_png.py --batch "📦:package,🚀:rocket" --folder release_assets --quiet
```

Runtime log entries are still persisted when warnings, errors, overwrites, or operational events are collected.

## Margin Controls

Use `--margin` when a fixed margin ratio is required:

```powershell
python unicode_to_png.py --emoji "🎯" --folder centered_icon --margin 0.2
```

Use `--autofixmargin` to enable edge detection and retry rendering with an increased margin when needed:

```powershell
python unicode_to_png.py --emoji "👨‍🚀" --folder astronaut --autofixmargin
```

## Memory Monitoring

Use `--memlimit` when optional memory monitoring is needed:

```powershell
python unicode_to_png.py --batch "🧠:brain,🧪:science" --folder edu_pack --memlimit 500
```

Memory monitoring requires `psutil`. If `psutil` is not installed, the CLI reports a warning and continues without memory monitoring.

## Common Errors

Missing emoji or batch input:

```powershell
python unicode_to_png.py
```

Result:

```text
[utp] - ERROR - No emoji input was provided. Use --emoji or --batch.
```

Missing output folder:

```powershell
python unicode_to_png.py --emoji "🎯"
```

Result:

```text
[utp] - ERROR - No output folder name was provided. Use --folder.
```

Invalid emoji input:

```powershell
python unicode_to_png.py --emoji "abc" --folder invalid_icon
```

Result:

```text
[utp] - ERROR - Invalid emoji input: 'abc'.
```

## Help Commands

Show command-line help:

```powershell
python unicode_to_png.py --help
```

Show detailed examples:

```powershell
python unicode_to_png.py --examples
```

Show the CLI version:

```powershell
python unicode_to_png.py --version
```
