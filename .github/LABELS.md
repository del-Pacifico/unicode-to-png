# Labels

This repository uses scoped labels to keep issues and pull requests predictable, searchable, and easy to triage.

Labels are grouped by family:

- `behavior:` describes compatibility and activation behavior.
- `dev:` describes development workflow state.
- `needs:` describes missing information or required pre-work.
- `priority:` describes urgency.
- `scope:` describes the affected project area.
- `status:` describes review, QA, or resolution state.
- `type:` describes the kind of work.

`.github/labels.yml` is the technical source of truth. GitHub does not apply this file automatically; labels must be created or updated through the GitHub UI, GitHub CLI, API, or a sync script.

## Synchronization

Use the repository sync script to preview and apply label changes through GitHub CLI:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/sync_github_labels.py --repo del-Pacifico/unicode-to-png
python scripts/sync_github_labels.py --repo del-Pacifico/unicode-to-png --apply
```

The script runs in dry-run mode by default. Remote labels that are not defined in `.github/labels.yml` are reported and left unchanged unless `--delete-extra --apply` is used.

| Name | Description | Color |
|------|-------------|-------|
| `behavior: non-breaking` | Changes that do not modify default behavior or break existing workflows. | `#20C997` |
| `behavior: opt-in` | Features disabled by default and enabled only by explicit user action. | `#6610F2` |
| `dev: ready` | Design approved and scope defined. Ready to start development. | `#F93F1F` |
| `dev: blocked` | Blocked by a dependency, decision, or external constraint. | `#D1242F` |
| `dev: in-progress` | Development is actively in progress. | `#D2F97F` |
| `dev: ready-for-review` | Implementation completed and ready for review or QA. | `#553458` |
| `needs: triage` | Needs initial review and categorization before being prioritized. | `#FBCA04` |
| `needs: reproduction` | Needs clear steps to reproduce the issue before it can be fixed. | `#C2E0C6` |
| `needs: design` | Requires design, UX, or CLI contract input before implementation. | `#5319E7` |
| `priority: high` | Critical issue with immediate impact; must be resolved as soon as possible. | `#E11D21` |
| `priority: normal` | Standard priority; should be addressed in the normal development cycle. | `#116045` |
| `priority: low` | Minor issue with little impact; can be postponed if needed. | `#A6A09B` |
| `scope: cli` | CLI arguments, command behavior, help output, and user-facing command flow. | `#0D6EFD` |
| `scope: rendering` | Emoji rendering, resizing, margins, clipping, and PNG generation behavior. | `#FD7E14` |
| `scope: unicode` | Unicode validation, emoji classification, ZWJ, modifiers, and emoji data. | `#0AA2C0` |
| `scope: font-backend` | Font loading, font fallback, Segoe UI Emoji, and future backend support. | `#6F42C1` |
| `scope: output-files` | Generated PNG names, output folders, artifacts, and file overwrite behavior. | `#198754` |
| `scope: batch-processing` | Batch parsing, aliases, multi-emoji processing, and partial batch continuity. | `#28A745` |
| `scope: logging` | Console messages, log files, severity levels, and diagnostic detail. | `#343A40` |
| `scope: filesystem` | Filesystem paths, folder creation, permissions, and IO error handling. | `#5A6268` |
| `scope: tests` | Unit tests, CLI tests, integration tests, fixtures, and regression coverage. | `#7057FF` |
| `scope: ci` | GitHub Actions, CI checks, build jobs, and automated validation. | `#17A2B8` |
| `scope: documentation` | README, usage guide, changelog, examples, and repository documentation. | `#006B75` |
| `scope: packaging` | Project metadata, package installation, entry points, wheels, or binaries. | `#6610F2` |
| `scope: dependencies` | Runtime and development dependency constraints or dependency updates. | `#0366D6` |
| `scope: release` | Release preparation, versioning, changelog finalization, and tagging. | `#6C757D` |
| `scope: repo-maintenance` | Repository maintenance such as labels, templates, gitignore, and branch hygiene. | `#ADB5BD` |
| `scope: security` | Security-sensitive behavior, dependency risk, privacy, or safe failure handling. | `#B60205` |
| `status: ready-for-review` | Ready for review; implementation completed and awaiting validation. | `#0D6EFD` |
| `status: ready-for-merge` | Approved and validated, ready for final merge into the target branch. | `#0E8A16` |
| `status: in-qa` | Implementation is under QA validation before final approval or merge. | `#C27AFF` |
| `status: blocked-by-conflict` | Cannot be merged due to branch conflicts; requires synchronization. | `#E5533D` |
| `status: backlog` | Approved but not yet scheduled for implementation. | `#6A737D` |
| `status: good first issue` | Suitable for newcomers; small and well-defined scope. | `#7057FF` |
| `status: duplicate` | Issue or PR already exists and will be closed as duplicate. | `#F28155` |
| `status: invalid` | Not valid, not reproducible, wrong repo, or incomplete. | `#E4E669` |
| `status: question` | Further information is requested; support or clarification is needed. | `#D876E3` |
| `status: wontfix` | Will not be worked on or merged. | `#2CCE03` |
| `status: help wanted` | Extra attention or community help is welcome. | `#008672` |
| `type: release` | Tasks related to preparing, tagging, or publishing a release. | `#1D76DB` |
| `type: chore` | Routine maintenance tasks with no feature impact. | `#CFD3D7` |
| `type: bug` | A confirmed defect causing incorrect or unexpected behavior. | `#D73A4A` |
| `type: feature` | A new functionality or significant enhancement. | `#0E8A16` |
| `type: hotfix` | Urgent fix applied directly to production or a release branch. | `#B60205` |
| `type: documentation` | Documentation-related changes or issues. | `#006B75` |
| `type: performance` | Performance or stability issue related to CPU, memory, IO, or long runs. | `#C2E0C6` |
| `type: investigation` | Pre-triage investigation to gather evidence before classification. | `#5319E7` |
| `type: edge-case` | Non-blocking behavior under specific or uncommon conditions. | `#FBCA04` |
