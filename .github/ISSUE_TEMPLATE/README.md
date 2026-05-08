# Issue Templates

This folder centralizes the issue forms and maintenance templates used by **Unicode to PNG**.
All issues and pull requests must be written in **English** and follow these templates when applicable.

---

## Available Templates

- **Bug report** - Use [`bug_report.yml`](./bug_report.yml) to report confirmed or suspected defects with reproduction steps, expected behavior, actual behavior, logs, and environment details.
- **Feature request** - Use [`feature_request.yml`](./feature_request.yml) to propose new capabilities with clear motivation, scope, expected behavior, and acceptance criteria.
- **Documentation** - Use [`documentation.yml`](./documentation.yml) to report missing, outdated, unclear, or incorrect documentation.
- **Edge case** - Use [`edge_case.yml`](./edge_case.yml) to document non-blocking behavior under uncommon inputs, folders, Unicode sequences, or runtime conditions.
- **Investigation** - Use [`investigation.yml`](./investigation.yml) when evidence must be gathered before classifying the work as a bug, feature, performance issue, or documentation change.
- **Performance or stability** - Use [`performance_stability.yml`](./performance_stability.yml) for CPU, memory, IO, long-running batch, or reliability concerns.
- **Hotfix** - Use [`hotfix.md`](./hotfix.md) for urgent, scoped fixes to critical problems in production or release branches.
- **Release checklist** - Use [`release_checklist.md`](./release_checklist.md) to prepare and track a new tagged release end-to-end.

> Pick the template that best fits your case. One issue = one purpose.

---

## Global Configuration

This directory is governed by [`config.yml`](./config.yml), which defines global behavior for templates. Typical fields include:

- `blank_issues_enabled`: whether users can open blank issues or must choose a template.
- `contact_links`: optional links for discussions, security, or documentation shown on "New issue".
- Default labels, assignees, and other metadata for issue routing (if configured).

> Do not edit `config.yml` without maintainer approval.

---

## How To Use

1. On GitHub, go to **Issues > New issue** and select a template.
2. Fill out all required sections. Keep your writing concise and action-oriented.
3. Do **not** remove default labels set by the template; they support triage and reporting.
4. Prefer one issue per change or concern to keep scope small and reviews efficient.

---

## Labels

The canonical label taxonomy is documented in [`../LABELS.md`](../LABELS.md), with machine-readable definitions in [`../labels.yml`](../labels.yml).

- **behavior:** default behavior impact, such as `behavior: non-breaking` or `behavior: opt-in`.
- **dev:** development workflow state, such as `dev: ready`, `dev: in-progress`, or `dev: blocked`.
- **needs:** missing information or required pre-work, such as `needs: triage` or `needs: reproduction`.
- **priority:** urgency, such as `priority: high`, `priority: normal`, or `priority: low`.
- **scope:** affected project area, such as `scope: cli`, `scope: rendering`, `scope: tests`, or `scope: repo-maintenance`.
- **status:** lifecycle state, such as `status: backlog`, `status: in-qa`, or `status: ready-for-merge`.
- **type:** work category, such as `type: bug`, `type: feature`, `type: documentation`, or `type: release`.

> Maintainers may add/remove labels during triage to reflect the current state.

---

## Triage Policy

- New issues are reviewed under **`needs: triage`**.
- Priorities are assigned based on impact, severity, and blast radius.
- Hotfix scope must stay minimal (no refactors or opportunistic changes).
- Maintainers may replace broad template labels with precise scope, status, behavior, and priority labels after review.

---

## Definition Of Done

- All checklist items in the chosen template are complete.
- Linked PRs and related issues are referenced in the issue or PR body.
- Tests and manual verification steps are documented and reproducible.
- If applicable, rollback plan and risk assessment are present.

---

## Useful Links

- **Contributing Guide**: `CONTRIBUTING.md`  
- **Security Policy**: `SECURITY.md`  
- **Code of Conduct**: `CODE_OF_CONDUCT.md`
