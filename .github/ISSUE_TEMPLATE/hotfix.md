---
name: "Hotfix"
about: "Urgent, minimal fix for a critical issue in production or a release branch"
title: "[HOTFIX] <short, imperative title>"
labels: ["type: hotfix", "needs: triage", "priority: high"]
assignees: []
---

<!--
Guidelines:
- Keep scope minimal; no refactors or opportunistic changes.
- Provide reproducible steps, risks, rollback plan, and test plan.
- Code must follow project standards (Python 3.11, Pillow 11.2.1, Google-style docstrings, professional error handling, console logs with begin...end).
- All content in English.
-->

## Summary

A concise description of the issue and the minimal fix.

## Impact & Severity

- **User-facing impact:** <what breaks / degraded behavior>
- **Severity:** <blocker | critical | major>
- **Blast radius:** <who/what is affected>

## Affected Scope

- **Modules/Files:** <list>
- **Versions/Tags/Branches:** <e.g., main, dev, v1.12>
- **Environments:** <Windows 10 Pro, etc.>

## Steps to Reproduce

1. <step>
2. <step>
3. <step>

**Expected:** <what should happen>  
**Actual:** <what happens instead>

## Diagnostics

- **Logs / Screenshots / Tracebacks:** <attach or paste key lines>  
- **Related Issues/PRs:** <links>  
- **Recent Changes (suspects):** <links or notes>

## Root Cause Hypothesis

Explain the likely cause in one or two paragraphs. Link to code lines if possible.

## Proposed Fix (Minimal)

- **Approach:** <what will be changed and why it’s the smallest viable change>  
- **Non-goals:** <what will NOT be addressed in this hotfix>

## Risk Assessment

- **Risk level:** <low | medium | high>  
- **Risk factors:** <e.g., affects core path, file I/O, CLI parsing>  
- **Mitigations:** <feature flag, guard rails, extra validation>

## Rollback Plan

- **How to revert:** <git steps or config to disable>  
- **Fallback behavior:** <safe degraded mode if applicable>

## Test Plan

- **Unit/Functional tests:** <cases to add or run>  
- **Manual verification steps:** <exact commands / scenarios>  
- **Edge cases:** <list at least 2–3>

## Release Plan

- **Target branch:** <e.g., release/x.y.z or main>  
- **Backport needed?** <yes/no — list branches>  
- **Version bump/changelog:** <yes/no — link to CHANGELOG.md entry>  
- **Tag:** <e.g., v1.12.1>

## Timeline (optional)

- <YYYY-MM-DD HH:MM> Detected
- <YYYY-MM-DD HH:MM> Diagnosed
- <YYYY-MM-DD HH:MM> Fixed
- <YYYY-MM-DD HH:MM> Released

## Checklist

- [ ] Scope is minimal; no refactors or unrelated changes.
- [ ] Repro steps provided and verified.
- [ ] Root cause hypothesis documented.
- [ ] Risks and mitigations documented.
- [ ] Rollback plan documented and tested (if feasible).
- [ ] Test plan covers success, failure, and edge cases.
- [ ] Code follows project standards (Google-style docstrings, error handling, **begin...end** logs).
- [ ] Security and privacy considerations reviewed.
- [ ] CHANGELOG updated (if applicable).
- [ ] Release plan agreed and communicated.
