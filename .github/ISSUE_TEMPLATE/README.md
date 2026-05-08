# Issue Templates

This folder centralizes the issue templates used by **Unicode to PNG**.  
All issues and pull requests must be written in **English** and follow these templates when applicable.

---

## Available templates

- **Bug report** — Use [`bug_report.md`](./bug_report.md) to report defects with steps to reproduce, expected vs actual behavior, logs, and environment details.
- **Feature request** — Use [`feature_request.md`](./feature_request.md) to propose new capabilities with clear motivation, scope, acceptance criteria, and alternatives considered.
- **Hotfix** — Use [`hotfix.md`](./hotfix.md) for urgent, scoped fixes to critical problems in production or release branches.
- **Release Checklist** — Use [`release_checklist.md`](./release_checklist.md) to prepare and track a new tagged release end-to-end.

> Pick the template that best fits your case. One issue = one purpose.

---

## Global configuration

This directory is governed by [`config.yml`](./config.yml), which defines global behavior for templates. Typical fields include:

- `blank_issues_enabled`: whether users can open blank issues or must choose a template.  
- `contact_links`: optional links for discussions, security, or documentation (shown on “New issue”).  
- Default labels, assignees, and other metadata for issue routing (if configured).

> Do not edit `config.yml` without maintainer approval.

---

## How to use

1) On GitHub, go to **Issues → New issue** and select a template.  
2) Fill out all required sections. Keep your writing concise and action-oriented.  
3) Do **not** remove default labels set by the template (they help triage and reporting).  
4) Prefer one issue per change/concern to keep scope small and reviews efficient.

---

## Labels (conventions)

- **type:** `type: bug`, `type: feature`, `type: hotfix`, `type: release`  
- **priority:** `priority: high`, `priority: normal`, `priority: low`  
- **status/needs:** `needs: triage`

> Maintainers may add/remove labels during triage to reflect the current state.

---

## Triage policy (short)

- New issues are reviewed under **`needs: triage`**.  
- Priorities are assigned based on impact, severity, and blast radius.  
- Hotfix scope must stay minimal (no refactors or opportunistic changes).

---

## Definition of Done (generic)

- ✅ All checklist items in the chosen template are complete.  
- ✅ Linked PRs and related issues are referenced in the **Links** section.  
- ✅ Tests and manual verification steps are documented and reproducible.  
- ✅ If applicable, **rollback plan** and **risk assessment** are present.

---

## Useful links

- **Contributing Guide**: `CONTRIBUTING.md`  
- **Security Policy**: `SECURITY.md`  
- **Code of Conduct**: `CODE_OF_CONDUCT.md`
