"""Version helpers for Unicode to PNG."""

from pathlib import Path


def read_version(root_dir=None):
    """Read the project version from the root VERSION file."""
    base_dir = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[1]
    version_file = base_dir / "VERSION"
    try:
        version = version_file.read_text(encoding="utf-8").strip()
        return version or "0.0.0"
    except OSError:
        return "0.0.0"
