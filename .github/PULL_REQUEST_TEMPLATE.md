# Pull Request Template - Unicode to PNG

## Summary

Describe the change in one or two clear paragraphs.

## Scope

- **Type:** `type: bug` / `type: feature` / `type: documentation` / `type: chore` / `type: performance` / `type: release` / other:
- **Scope:** `scope: cli` / `scope: rendering` / `scope: unicode` / `scope: output-files` / `scope: tests` / `scope: documentation` / `scope: repo-maintenance` / other:
- **Behavior:** `behavior: non-breaking` / `behavior: opt-in` / breaking change:
- **Priority:** `priority: high` / `priority: normal` / `priority: low`

## Labels

Apply the appropriate repository labels before requesting review.

This repository uses a scoped label taxonomy documented in `.github/LABELS.md`. Pull requests without accurate labels may be rejected or returned for triage before review.

Minimum expected labels:

- One `type:` label.
- At least one `scope:` label.
- One `priority:` label.
- One `behavior:` label when compatibility or default behavior is relevant.
- One `status:` label that reflects the current review state.

Examples:

```text
type: chore
scope: dependencies
priority: normal
behavior: non-breaking
status: ready-for-review
```

## Branch Flow

This repository follows a staged promotion flow:

```text
feature/chore branch -> dev -> main -> tag/release
```

Rules:

- Open feature, chore, fix, docs, test, and refactor PRs against `dev`.
- Promote `dev` to `main` only through a dedicated release promotion PR.
- Create tags and GitHub Releases only after the release promotion PR has been merged into `main`.
- Do not open work branches directly against `main` unless the PR is an approved hotfix.
- Hotfix PRs must stay minimal, use explicit labels, and include rollback notes.

## Related Issues

Closes #
Relates to #

## Changes

-

## Validation

List exact commands and manual checks performed.

```powershell
python -m compileall unicode_to_png.py unicode_to_png tests
python -m pytest
python .\unicode_to_png.py --help
```

## Risk And Impact

- **Performance:**
- **Stability:**
- **Security:**
- **Compatibility:**
- **Rollback:**

## Documentation

- [ ] `README.md` updated or confirmed unchanged.
- [ ] `CHANGELOG.md` updated or confirmed unchanged.
- [ ] Usage examples updated or confirmed unchanged.
- [ ] GitHub templates, labels, or workflow docs updated when repository governance changed.

## Checklist

- [ ] Code follows the project style and supported Python version policy.
- [ ] User-facing CLI messages, code comments, and console logs are written in professional English.
- [ ] Errors are handled with clear user output and detailed operational logs when applicable.
- [ ] Edge cases preserve flow continuity where possible and emit warnings when applicable.
- [ ] No sensitive information, generated runtime artifacts, or local analysis reports are included.
- [ ] Tests or documented manual validation cover the changed behavior.
- [ ] Required labels were applied and match `.github/LABELS.md`.
- [ ] This PR targets the correct base branch according to the branch flow.
- [ ] If this PR targets `main`, it is a release promotion or approved hotfix.
