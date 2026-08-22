---
name: critical-path-task-run
description: Use when implementing Critical Path / critical-path-dj feature work, bug fixes, UI changes that must preserve the frontend design system, Django changes, migrations, review fixes, or tasks that mention critical-path-guidelines, MannyAI, Pattern, factories, brands, orders, BOM, CAD, drops, or stages.
---

# Critical Path Task Run

## Overview

Run Critical Path work as a production-safe delivery loop: clarify business behavior first, reuse existing paths, make the smallest code change, verify, then report in business language before technical detail.

## Required sub-skill

Use `$critical-path-guidelines` whenever available. It contains the repo-specific rules and overrides this guide if there is a conflict.

## Workflow

1. **Intake**
   - Translate the request into: objective, user/workflow impact, exact behavior change, and what must not change.
   - If the request contains meeting notes or review text, extract only actionable product requirements.
   - Classify tenant scope as ASOS-only, TechnoSport-only, or shared; state the intended brand and factory behavior.
   - Identify every synchronized user-facing surface or API entry point that must show the changed state, including any required two-way synchronization.
   - Ask before changing permissions, roles, API contracts, serializer/service boundaries, migrations, failure semantics, or unclear business rules.

2. **Branch and workspace safety**
   - For Critical Path app repositories, default base is `dev` unless the user names another base. If the repository path is not already clear from the session, inspect the current workdir or ask before changing branches.
   - Before edits: fetch, checkout/update the intended base, then create or confirm the feature branch.
   - Use neutral branch names only: `feat/<short-description>` for features and `fix/<short-description>` for bug fixes. Never use AI, editor, tool, or automation-branded prefixes, even if a platform default suggests them.
   - If the worktree is dirty or branch intent is ambiguous, stop and report the blocker.

3. **Implementation discipline**
   - Reuse existing views, serializers, services, templates, JS modules, tests, and UI patterns first.
   - For UI work, inspect comparable screens, nearby templates, CSS/theme files, static JS modules, and active component patterns before editing.
   - Preserve existing design principles, CSS variables/classes, color semantics, component patterns, JS helpers, accessibility, and responsive behavior.
   - Do not introduce unapproved UI libraries, CSS frameworks, palettes, fonts, icon sets, animation libraries, bundlers, or one-off visual systems.
   - Keep the diff minimal. Do not rename, reformat, remove code, or reshape working logic unless required.
   - Never hand-write Django migrations; use `uv run python manage.py makemigrations`.
   - Prefer local non-Docker commands with `DJANGO_READ_DOT_ENV_FILE=true`.

4. **Verification**
   - Run the smallest meaningful tests/checks first; expand only if risk justifies it.
   - For UI work, verify the relevant page or at least inspect the JS/template path.
   - Verify both brand and factory journeys; for deliberately role-scoped work, verify the other role is unchanged.
   - Verify every synchronized surface identified during intake, including persisted/two-way behavior where applicable.
   - Before handoff, verify no unapproved UI library, palette, font, icon set, framework, or visual language was introduced.
   - Review `git diff --stat`, `git diff --name-only`, and the full diff for scope drift.

## Final response

Use this order:
- what changed
- why it changed, in PM/business language
- how to verify quickly
- technical notes only where helpful
- risks or assumptions

## Common mistakes

| Mistake | Fix |
|---|---|
| Treating meeting transcript as one big spec | Extract actionable requirements and ignore chatter. |
| Starting from current feature branch by accident | Reset to the intended base first. |
| Solving with a new abstraction | Reuse existing local patterns unless required. |
| Reporting only files changed | Explain business/user/workflow impact first. |
