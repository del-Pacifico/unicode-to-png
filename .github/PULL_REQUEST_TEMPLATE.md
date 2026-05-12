# 🧙🏻‍♂️ Pull Request Template - Unicode to PNG

## Summary

Describe the change in one or two clear paragraphs. Explain what problem this PR solves and why the change is needed.

## Impact Summary

Describe the practical scope of this PR.

- **Change type:** bug fix / feature / chore / documentation / test / release / hotfix / other:
- **Primary area affected:** CLI / rendering / Unicode handling / output files / tests / documentation / dependencies / release / repository maintenance / other:
- **User-facing impact:** none / low / medium / high:
- **Compatibility impact:** non-breaking / opt-in / breaking:
- **Operational impact:** none / CI only / release only / runtime behavior / maintenance workflow:

## Labels

Apply the appropriate repository labels before requesting review.

This repository uses a scoped label taxonomy documented in `.github/LABELS.md`. Pull requests without accurate labels may be rejected or returned for triage before review.

Minimum expected labels:

- One `type:` label.
- At least one `scope:` label.
- One `priority:` label.
- One `behavior:` label when compatibility or default behavior is relevant.
- One `status:` label that reflects the current review state.

Example:

```text
type: chore
scope: dependencies
priority: normal
behavior: non-breaking
status: ready-for-review
```

## Branch Flow

Confirm that this PR follows the repository promotion flow.

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

List related issues, discussions, or PRs. Use closing keywords only when this PR fully resolves the issue.

```text
Closes #
Relates to #
Supersedes #
```

## Changes

List the concrete changes introduced by this PR. Use `Not applicable` for categories that do not apply.

- **Code:**
- **Tests:**
- **Documentation:**
- **Repository/GitHub configuration:**
- **Dependencies:**

## Validation

List exact commands and manual checks performed. Include results, not just commands.

```powershell
python -m compileall unicode_to_png.py unicode_to_png tests
python -m pytest
python .\unicode_to_png.py --help
python .\unicode_to_png.py --version
```

## Risk And Impact

Document concrete risks and mitigations. Use `None` only when the category was reviewed and does not apply.

- **Performance:**
- **Stability:**
- **Security:**
- **Compatibility:**
- **Rollback:**

## Documentation

Confirm documentation impact. Update documentation when behavior, dependencies, usage, release metadata, or repository governance changes.

- [ ] `README.md` updated or confirmed unchanged.
- [ ] `CHANGELOG.md` updated or confirmed unchanged.
- [ ] Usage examples updated or confirmed unchanged.
- [ ] GitHub templates, labels, or workflow docs updated when repository governance changed.

## Checklist

Confirm every applicable item before requesting review.

- [ ] Code follows the project style and supported Python version policy.
- [ ] User-facing CLI messages, code comments, and console logs are written in professional English.
- [ ] Errors are handled with clear user output and detailed operational logs when applicable.
- [ ] Edge cases preserve flow continuity where possible and emit warnings when applicable.
- [ ] No sensitive information, generated runtime artifacts, or local analysis reports are included.
- [ ] Tests or documented manual validation cover the changed behavior.
- [ ] Required labels were applied and match `.github/LABELS.md`.
- [ ] This PR targets the correct base branch according to the branch flow.
- [ ] If this PR targets `main`, it is a release promotion or approved hotfix.
