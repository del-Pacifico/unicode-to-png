# 📦 Changelog – Unicode to png

All notable changes to this project are documented in this file.  
This project follows [Semantic Versioning](https://semver.org/).

---

## [1.11] - 2025-04-16

### 🚀 Overview

This update focuses on polish, correctness, and usability across project metadata, documentation, and internal linking. It ensures a fully functional navigation experience in the README and aligns all files for GitHub publishing and open source maintainability.

---

### ✨ Added

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
