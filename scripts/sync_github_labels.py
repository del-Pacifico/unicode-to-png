## This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/
#
# Original Author: Sergio Palma Hidalgo
# Project URL: https://github.com/del-Pacifico/unicode-to-png
# Copyright (c) 2025 Sergio Palma Hidalgo
# All rights reserved.
#

"""Synchronize GitHub repository labels from .github/labels.yml."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


LOG_PREFIX = "[utp-labels]"
DEFAULT_REPOSITORY = "del-Pacifico/unicode-to-png"
DEFAULT_LABELS_FILE = Path(".github") / "labels.yml"
HEX_COLOR_PATTERN = re.compile(r"^[0-9A-Fa-f]{6}$")


class LabelSyncError(RuntimeError):
    """Raised when label synchronization cannot continue safely."""


def write_console(level: str, message: str) -> None:
    """Write a deterministic console message with the repository tooling prefix."""

    print(f"{LOG_PREFIX} - {level.upper()} - {message}")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize GitHub labels from .github/labels.yml.",
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPOSITORY,
        help=f"GitHub repository in owner/name format. Default: {DEFAULT_REPOSITORY}.",
    )
    parser.add_argument(
        "--labels-file",
        default=str(DEFAULT_LABELS_FILE),
        help=f"Path to the label definition file. Default: {DEFAULT_LABELS_FILE}.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to GitHub. Without this flag, the script only prints a dry run.",
    )
    parser.add_argument(
        "--delete-extra",
        action="store_true",
        help="Delete remote labels that are not present in the labels file. Requires --apply.",
    )
    return parser.parse_args(argv)


def load_label_definitions(labels_file: Path) -> List[Dict[str, str]]:
    if not labels_file.exists():
        raise LabelSyncError(f"Label definition file was not found: {labels_file}")

    try:
        import yaml
    except ImportError as exc:
        raise LabelSyncError(
            "PyYAML is required to read label definitions. "
            "Install development dependencies with: python -m pip install -r requirements-dev.txt"
        ) from exc

    try:
        with labels_file.open("r", encoding="utf-8") as handle:
            raw_labels = yaml.safe_load(handle)
    except OSError as exc:
        raise LabelSyncError(f"Unable to read label definition file: {exc}") from exc
    except yaml.YAMLError as exc:
        raise LabelSyncError(f"Invalid YAML in label definition file: {exc}") from exc

    return validate_label_definitions(raw_labels)


def validate_label_definitions(raw_labels: Any) -> List[Dict[str, str]]:
    if not isinstance(raw_labels, list):
        raise LabelSyncError("Label definition file must contain a YAML list.")

    labels: List[Dict[str, str]] = []
    seen_names = set()

    for index, raw_label in enumerate(raw_labels, start=1):
        if not isinstance(raw_label, Mapping):
            raise LabelSyncError(f"Label entry #{index} must be a mapping.")

        normalized = {}
        for key in ("name", "description", "color"):
            value = raw_label.get(key)
            if not isinstance(value, str) or not value.strip():
                raise LabelSyncError(f"Label entry #{index} has an invalid '{key}' value.")
            normalized[key] = value.strip()

        if normalized["name"] in seen_names:
            raise LabelSyncError(f"Duplicate label definition found: {normalized['name']}")
        seen_names.add(normalized["name"])

        if not HEX_COLOR_PATTERN.match(normalized["color"]):
            raise LabelSyncError(
                f"Label '{normalized['name']}' has invalid color '{normalized['color']}'. "
                "Use exactly six hexadecimal characters without '#'."
            )

        labels.append(normalized)

    if not labels:
        raise LabelSyncError("Label definition file does not contain any labels.")

    return labels


def ensure_gh_cli_available() -> None:
    if shutil.which("gh") is None:
        raise LabelSyncError("GitHub CLI was not found in PATH. Install and authenticate 'gh' first.")


def run_gh(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    command = ["gh", *args]
    try:
        return subprocess.run(command, capture_output=True, check=False, text=True)
    except OSError as exc:
        raise LabelSyncError(f"Unable to execute GitHub CLI: {exc}") from exc


def fetch_remote_labels(repository: str) -> Dict[str, Dict[str, str]]:
    result = run_gh(
        [
            "label",
            "list",
            "--repo",
            repository,
            "--limit",
            "1000",
            "--json",
            "name,description,color",
        ]
    )
    if result.returncode != 0:
        raise LabelSyncError(
            "Unable to fetch remote labels from GitHub. "
            f"GitHub CLI returned: {result.stderr.strip() or result.stdout.strip()}"
        )

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise LabelSyncError(f"GitHub CLI returned invalid JSON: {exc}") from exc

    remote_labels: Dict[str, Dict[str, str]] = {}
    for item in payload:
        if not isinstance(item, Mapping) or not isinstance(item.get("name"), str):
            raise LabelSyncError("GitHub CLI returned an unexpected label payload.")
        remote_labels[item["name"]] = {
            "name": item["name"],
            "description": str(item.get("description") or ""),
            "color": str(item.get("color") or "").lstrip("#"),
        }

    return remote_labels


def compare_labels(
    desired_labels: Iterable[Mapping[str, str]],
    remote_labels: Mapping[str, Mapping[str, str]],
) -> Tuple[List[Mapping[str, str]], List[Mapping[str, str]], List[str]]:
    create_actions: List[Mapping[str, str]] = []
    update_actions: List[Mapping[str, str]] = []

    for desired in desired_labels:
        remote = remote_labels.get(desired["name"])
        if remote is None:
            create_actions.append(desired)
            continue

        remote_color = remote["color"].lower()
        desired_color = desired["color"].lower()
        if remote.get("description", "") != desired["description"] or remote_color != desired_color:
            update_actions.append(desired)

    desired_names = {label["name"] for label in desired_labels}
    extra_labels = sorted(name for name in remote_labels if name not in desired_names)

    return create_actions, update_actions, extra_labels


def apply_label_create(repository: str, label: Mapping[str, str]) -> None:
    result = run_gh(
        [
            "label",
            "create",
            label["name"],
            "--repo",
            repository,
            "--description",
            label["description"],
            "--color",
            label["color"],
        ]
    )
    if result.returncode != 0:
        raise LabelSyncError(f"Unable to create label '{label['name']}': {result.stderr.strip()}")


def apply_label_update(repository: str, label: Mapping[str, str]) -> None:
    result = run_gh(
        [
            "label",
            "edit",
            label["name"],
            "--repo",
            repository,
            "--description",
            label["description"],
            "--color",
            label["color"],
        ]
    )
    if result.returncode != 0:
        raise LabelSyncError(f"Unable to update label '{label['name']}': {result.stderr.strip()}")


def apply_label_delete(repository: str, label_name: str) -> None:
    result = run_gh(["label", "delete", label_name, "--repo", repository, "--yes"])
    if result.returncode != 0:
        raise LabelSyncError(f"Unable to delete label '{label_name}': {result.stderr.strip()}")


def report_actions(
    create_actions: Sequence[Mapping[str, str]],
    update_actions: Sequence[Mapping[str, str]],
    extra_labels: Sequence[str],
    apply_changes: bool,
    delete_extra: bool,
) -> None:
    mode = "apply" if apply_changes else "dry-run"
    write_console(
        "info",
        (
            f"Label synchronization plan generated in {mode} mode: "
            f"{len(create_actions)} to create, {len(update_actions)} to update, "
            f"{len(extra_labels)} remote labels not defined locally."
        ),
    )

    for label in create_actions:
        write_console("info", f"Create label: {label['name']}")
    for label in update_actions:
        write_console("info", f"Update label: {label['name']}")
    for label_name in extra_labels:
        level = "warning" if delete_extra else "info"
        action = "Delete extra label" if delete_extra else "Extra remote label left unchanged"
        write_console(level, f"{action}: {label_name}")


def synchronize_labels(
    repository: str,
    labels_file: Path,
    apply_changes: bool,
    delete_extra: bool,
) -> None:
    if delete_extra and not apply_changes:
        raise LabelSyncError("--delete-extra requires --apply to avoid accidental destructive changes.")

    desired_labels = load_label_definitions(labels_file)
    ensure_gh_cli_available()

    write_console("info", f"Fetching current labels from {repository}.")
    remote_labels = fetch_remote_labels(repository)
    create_actions, update_actions, extra_labels = compare_labels(desired_labels, remote_labels)
    report_actions(create_actions, update_actions, extra_labels, apply_changes, delete_extra)

    if not apply_changes:
        write_console("info", "Dry run completed. Re-run with --apply to modify GitHub labels.")
        return

    for label in create_actions:
        apply_label_create(repository, label)
        write_console("info", f"Created label: {label['name']}")

    for label in update_actions:
        apply_label_update(repository, label)
        write_console("info", f"Updated label: {label['name']}")

    if delete_extra:
        for label_name in extra_labels:
            apply_label_delete(repository, label_name)
            write_console("warning", f"Deleted extra label: {label_name}")

    write_console("info", "GitHub label synchronization completed.")


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    try:
        synchronize_labels(
            repository=args.repo,
            labels_file=Path(args.labels_file),
            apply_changes=args.apply,
            delete_extra=args.delete_extra,
        )
    except LabelSyncError as exc:
        write_console("error", str(exc))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
