# 📦 Changelog – Unicode to png

All notable changes to this project are documented in this file.  
This project follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### 🛠️ Fixed

- Corrected GitHub Actions workflow: updated `codeql-action` steps to use the correct `github/codeql-action` namespace. This resolves errors when executing `init@v2` and `analyze@v2`.

### ✨ Planned

- Support for custom image sizes via `--sizes` flag (TBD).
- Interactive mode fallback improvements (TBD).

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
