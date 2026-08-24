# Workflow B Router

Load this file first. It routes the agent without loading source cards or detailed theory.

## Routing

1. Identify the current SOP state from `L0/sop-state-machine.md`.
2. Select a project profile from `L0/project-profiles.md`.
3. Load the current state's `playbook.md`, `checklist.md`, and `methods-index.md`.
4. Enable only the cross-cutting modules triggered by the profile or current risk.
5. Load L2 methods or templates for the concrete activity.
6. Load L3 provenance only for traceability, disagreement, audit, or deep study.

## Loading Levels

```text
L0: route and decide
L1: execute the current state
L2: perform a method or use a template
L3: inspect evidence and source history
```

Do not load `registry/` or `sources/` during ordinary work.
