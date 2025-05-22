# 📦 Changelog – Unicode to png

All notable changes to this project are documented in this file.  
This project follows [Semantic Versioning](https://semver.org/).

---

## [1.19.1] - 2025-05-21

### 🔍 Review Summary

Patch release focused exclusively on documentation and metadata consistency.  
No source code logic has been changed.

---

### 📝 Changed

- **README.md**
  - ✅ Fixed anchor links in the Table of Contents to comply with GitHub slug rules.
  - ✏️ Adjusted Markdown anchors (removed emojis from slugs) for navigation consistency.

- **LICENSE**
  - 🔄 Updated repository reference to the correct GitHub organization:
    - From: `github.com/sergiopalmah/unicode_to_png`
    - To: `github.com/del-Pacifico/unicode_to_png`

- **SECURITY.md**
  - 🔄 Bumped `Supported Version` table from `1.12` to `1.19` to match latest release.

- **.gitignore**
  - ✏️ Added rules to exclude editor/IDE metadata: `.vs/`, `*.suo`, `*.db`, `*.vsidx`, etc.

---

### 🧾 Notes

This release ensures all documentation and security references are aligned with the organizational hosting and current project state.

No changes in emoji rendering logic, CLI behavior, or output files were introduced.

---

## 🧾 Changelog

### v1.19 — 2025-05-21

#### 🔍 Technical Review Summary (v1.19)

Unicode to PNG v1.19 introduces a robust and production-ready emoji rendering pipeline focused on stability, performance, and developer automation. The inclusion of smart margin correction, logging, and Unicode compliance transforms it into a professional tool for browser extension developers and designers alike.

Key architectural improvements include modularization of logic blocks, isolated error handling, and memory-safe canvas workflows. CI/CD readiness is achieved through silent mode, batch operations, and consistent output structure.

All code is now guided by strong engineering principles:
- Resilience to edge cases
- Predictable resource cleanup
- Defense against invalid input
- Log-auditable execution flows

---

#### ✨ Added

- `--autofixmargin` flag: auto-detects edge clipping and re-renders with padding.
- `--margin <float>`: allows manual margin setting (e.g., `--margin 0.25`).
- Unicode-aware rendering engine that supports:
  - Skin tone modifiers (`👍🏿`)
  - ZWJ sequences (`👩‍🚒`, `👨‍👩‍👧‍👦`)
  - Presentation selectors and flag tags
- Logging system that:
  - Records overwrites, warnings, and render issues.
  - Outputs log files to `log/YYYYMMDD_<folder>.log`
- CLI `--batch` support for emoji:alias pairs (e.g., `🔥:fire,🎨:palette`)
- Silent execution mode via `--quiet` (no console output, logs still saved).
- Folder/alias sanitization for filesystem-safe names.
- Modular structure with fully isolated functions:
  - `parse_args()`, `parse_batch()`, `load_font()`, `log()`, `prepare_log_path()`
- New section in README:
  - `💖 Support the Project` with donation badges and links.
- Added project-wide quality badges (privacy, modular design, AI-assisted).
- Section `🛡️ Engineering Principles` explaining performance and stability principles.

#### 🔄 Changed

- Emoji rendering now uses 4× resolution canvas and high-quality `Image.LANCZOS` downsampling.
- Bounding box calculation improved using `draw.textbbox()` for precision centering.
- Logging timestamps now follow format `[YYYY-MM-DD HH:MM:SS]`.
- Minimum Python version raised to `3.6+` (recommended `3.11+`).
- Font loading made fault-tolerant with fallback handling.
- Technical Design section expanded to include modular architecture, validations, and CLI design.
- README completely overhauled:
  - Sections rewritten: Description, Features, How It Works, Options, Use Cases
  - Added command-line usage examples for all flag combinations
  - Enhanced Table of Contents for accuracy and anchor sync

#### 🛠️ Fixed

- Bug where emojis were clipped at the top/right edges due to tight bounding box.
- Issue where ZWJ sequences produced misaligned output.
- Rendering errors that occurred silently without feedback are now logged properly.

### 🧹 Removed

- Implicit emoji rendering without input validation.
- Redundant or inconsistent print messages.
- Unclear margin handling logic replaced with formal CLI options.

#### 🔐 Security

- Emoji and folder inputs are fully sanitized (`[a-zA-Z0-9_]` only).
- No filesystem overwrite without clear log trace.
- All external input errors are isolated and reported gracefully.

---

## [Unreleased]

### 🛠️ Fixed

- Updated GitHub Actions workflow for CodeQL analysis:
  - Migrated from deprecated `@v2` to `@v3` (`init` and `analyze`).
  - Added required `permissions` block (`security-events: write`) to allow GitHub to process results.
  - Noted that CodeQL scanning results are only visible in repositories under a GitHub **Organization** account.

### 📘 Documentation

- Updated `README.md` with clarified AI badge groups and improved layout.
- Added `## 🏷️ Project Qualities` section to highlight privacy, modularity, and AI-assisted development.
- Linked `SECURITY.md` and `CONTRIBUTING.md` via a new section: `## 📚 Governance & Ethics`.
- Declared the use of tools like GitHub Copilot, ChatGPT (OpenAI), and Google Gemini in both policies.

### 🔧 Metadata & Style

- Maintained consistent badge styles and groupings.
- Ensured headers follow TOC-compatibility (e.g. badge sections are `##` level).
- Added markdown-friendly visual spacing between badge groups using `<br>` and comments.

### ℹ️ Notes

- Although CodeQL analysis runs correctly on push and pull requests, results will not appear in the **Security > Code scanning alerts** tab unless the repository belongs to a GitHub **Organization** account. This is a GitHub Advanced Security limitation.

---

## [1.12] - 2025-04-17

### 🐞 Bug Fixes

- Fixed a folder duplication bug where using `--folder fire` incorrectly created `fire_fire`. Now the folder is named exactly as provided by the user.
- Fixed missing emoji validation: the script now only accepts valid Unicode emoji symbols and rejects non-emoji characters (e.g., regular letters or punctuation).

### ✨ Features & Improvements

- Added full Unicode emoji validation using defined emoji Unicode blocks.
- Improved the `if __name__ == "__main__"` block:
  - Uncaught exceptions are now logged in a fallback file located at `log/YYYYMMDD_error.log`.
  - The script now exits with `sys.exit(1)` on failure, signaling errors properly to external scripts or CI pipelines.

### 📘 Documentation & Presentation

- Added a `Visual Preview` section to the `README.md` that includes:
  - `cli_demo.png`: Example of CLI usage
  - `output_preview.png`: Folder overview with generated emoji image set
  - `emoji_sizes_detail.png`: All PNG sizes produced from a sample emoji
- Clarified that only valid Unicode emoji are accepted as input (`README.md`, under How It Works).
- Added a footer badge block to visually highlight key project qualities: No tracking, Modular, Lightweight, Open Source.

### 🛡️ Security & Licensing

- License updated from **MIT** to **Mozilla Public License 2.0 (MPL-2.0)** to ensure proper attribution and openness while protecting original work.
- Updated project header badge to reflect MPL-2.0.
- Added recommended MPL license header block to the main script file (`unicode_to_png.py`), including author and GitHub project URL.

### 📁 Project Infrastructure

- Added `.github/FUNDING.yml` to support GitHub Sponsors.
- Added `.github/workflows/codeql.yml` to enable automatic CodeQL-based static security scanning for Python.

---

## [1.11] - 2025-04-16

### 🚀 Overview of Changes

This update focuses on polish, correctness, and usability across project metadata, documentation, and internal linking. It ensures a fully functional navigation experience in the README and aligns all files for GitHub publishing and open source maintainability.

---

### ✨ New Features

- **Status Badge:** Introduced `status: beta` badge to clarify project maturity.
- **Technical Summary & Description:** Added developer-focused metadata for GitHub repo creation.
- **Initial CHANGELOG.md File:** Structured changelog using semantic versioning, including detailed overview, modules added, infrastructure, and documentation highlights for v1.10.
- **Script Version Display:** Added version reference `v1.11` in the `print()` banner of `unicode_to_png.py`.

---

### 📝 Changed

- **README.md:**
  - Corrected all anchor links in the Table of Contents (`How It Works`, `Edge Cases`, platform subsections, etc.) to match GitHub rendering behavior.
  - Replaced fixed `main` branch changelog link with relative Markdown path for cross-branch compatibility.
  - Refined phrasing in the Installation section to eliminate redundant CLI notices.
- **LICENSE:**
  - Updated header from plain text to Markdown-style `# MIT License`.
  - Replaced copyright:
    - From: `SergioPalmaH`
    - To: `Unicode to PNG` for consistency with project identity.

---

### 🛠 Fixed

- Broken or unresolved internal links within `README.md`.
- Missing `CHANGELOG.md` file caused by GitHub anchor failure on new repos.

---

### 🧼 Improvements

- Clean Markdown formatting throughout all documentation blocks.
- Ensured internal anchors are fully GitHub-compatible.
- Improved structure and consistency for better rendering and accessibility.

---

### 📘 Post-release Updates (2025-04-17)

- Fixed broken Markdown anchors in the README Table of Contents (`How It Works`, `Options Available`, `Changelog`, etc.).
- Corrected internal headings to match GitHub anchor behavior.
- Updated `SECURITY.md` to reflect version `1.11` as the currently supported version.

---

## [1.10] - 2025-04-15

### 🚀 Overview

Initial public release of **Unicode to png**, a CLI tool written in Python that converts Unicode emoji into browser-compatible PNG icons. This version introduces full emoji rendering support, standardized output sizes, batch processing, structured logging, and GitHub community files for open source collaboration.

---

### ✨ Added

- **Command-line Interface (CLI)** with support for:
  - `--emoji` for single emoji rendering.
  - `--batch` for processing multiple emojis with alias support.
  - `--folder` to specify output location.
  - `--quiet` for silent operation in automation contexts.
- **Rendering Engine** using Pillow and Segoe UI Emoji:
  - High-resolution canvas rendering and downsampling via `Image.LANCZOS`.
  - Support for emojis using Zero Width Joiners (ZWJ).
- **Output Generation**:
  - PNG icon sizes: `16x16`, `19x19`, `32x32`, `38x38`, `48x48`, `128x128`.
  - Saved under `/emojis/<base>_<alias>/` with naming convention `emoji_{size}.png`.
- **Logging System**:
  - Log files are only created on warnings/errors.
  - Named as `YYYYMMDD_<folder>.log` in a dedicated `/log` directory.
- **Folder and filename sanitization** to prevent invalid characters and file conflicts.

---

### 🛠 Infrastructure & Tooling

- Created `.gitignore` to exclude `__pycache__`, `env/`, and temporary logs.
- Added `requirements.txt` with `Pillow>=9.0`.
- Verified Python 3.6+ compatibility.
- Modular structure with `main()`, `parse_args()`, `parse_batch()`, `load_font()`, and `log()`.

---

### 📄 Documentation & Community

#### ✅ Added

- `README.md` with:
  - Unicode emoji navigation and usage examples.
  - Architecture and rendering flow.
  - Recommended usage for CLI and automation.
- `LICENSE` under MIT License.
- `CHANGELOG.md` (this file).
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`.

#### 🗂️ .github directory

- `PULL_REQUEST_TEMPLATE.md` for standardized PRs.
- `ISSUE_TEMPLATE/`:
  - `bug_report.md` and `feature_request.md` for structured issue reporting.
  - `config.yml` to disable blank issues and provide guidance.

---

### 🧩 Known Limitations

- Emoji rendering may fail or appear monochrome on systems without Segoe UI Emoji or proper color font support.
- The script is optimized for Windows; Linux/macOS compatibility is limited to environments with custom font support.

---
