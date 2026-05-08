---
name: "Release Checklist"
about: "Plan and track a Unicode to PNG release end-to-end"
title: "[RELEASE] v<x.y.z> — YYYY-MM-DD"
labels: ["type: release", "scope: release", "needs: triage", "priority: normal"]
assignees: []
---

<!--
Guidelines:
- Keep the scope of the release focused and well-defined.
- Ensure code follows project standards, supported Python versions, declared dependency constraints, professional error handling, and objective console logs.
- All content in English.
-->

## Summary

Briefly describe the release goal(s), scope, and target date.

## Scope

- **In scope (must ship):**
  - <list features/fixes>
- **Out of scope (explicitly not included):**
  - <list items>

## Versioning

- [ ] Confirm the release version follows semantic versioning (x.y.z).
- [ ] Update version constant/file (if applicable) in the codebase.
- [ ] Update `CHANGELOG.md` with an **Added / Changed / Fixed / Removed** section for this version.

## Readiness (Code & Quality)

- [ ] All changes merged into the target branch (e.g., `main`) from reviewed PRs.
- [ ] Code follows project standards, robust error handling, and objective console logs.
- [ ] No TODOs or commented-out code left in release paths.
- [ ] Dependencies reviewed against `requirements.txt`, `requirements-dev.txt`, and `pyproject.toml`.
- [ ] Security/privacy review completed (no secrets, tokens, or sensitive data in repo or logs).

## Tests & Verification

- [ ] Unit/functional tests (if present) pass locally and in CI.
- [ ] Manual verification performed on supported environments (e.g., Windows 10 Pro).
- [ ] Edge cases validated (invalid Unicode, large batches, invalid output folder, permission errors).
- [ ] Error handling verified (clear messages, safe exits, no unhandled exceptions).
- [ ] Performance sanity check (reasonable time and memory for typical inputs).

## Docs & Repo Hygiene

- [ ] `README.md` updated for this release (usage, options, examples).  
- [ ] Internal links and anchors verified (Table of Contents works).
- [ ] Remove or update any outdated badges/sections (if applicable).
- [ ] `.github/ISSUE_TEMPLATE/README.md` lists current issue forms, maintenance templates, label conventions, and `config.yml`.
- [ ] `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` validated (no stale references).

## Packaging & Distribution (if applicable)

- [ ] Build artifacts prepared (source archive, wheels, or packaged binaries if used).
- [ ] Artifact names and checksums verified.
- [ ] Installation instructions tested against a clean environment.

## Release Notes

- [ ] Draft GitHub Release notes include:
  - Overview of changes (Added/Changed/Fixed/Removed)
  - Upgrade notes / breaking changes
  - Known issues and workarounds
- [ ] Links to related issues/PRs included.
- [ ] Screenshots or short examples (optional but recommended).

## Tag & Publish

- [ ] Create and push tag `v<x.y.z>` on the target branch.
- [ ] Publish GitHub Release with attached artifacts (if any).
- [ ] Verify the release page renders correctly and all links work.

## Post-Release

- [ ] Confirm users can run the new version (quick smoke test from a clean clone).
- [ ] Monitor for regressions or high-impact bug reports.
- [ ] If needed, open a follow-up issue for deferred items or documentation enhancements.

## Rollback Plan

- [ ] Document the rollback steps (git revert/tag delete or hotfix plan).
- [ ] Validate that previous stable version is still accessible and installable.

## Approvals

- [ ] Maintainer approval
- [ ] Security/privacy review (if applicable)
- [ ] Final sign-off

---

### Links

- Target branch: <link>
- Milestone: <link>
- Related issues/PRs: <links>
- Changelog entry: <link>
