# Workflow B Handbook Visibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Workflow B as a progressive-disclosure handbook with L0 routing, L1 state playbooks, L2 methods/templates, and L3 provenance references.

**Architecture:** Keep `registry/` and `sources/` intact as provenance/build data. Add an authoritative `workflow-b/manifest.yaml`, L0 router, state-specific L1 playbooks/checklists, cross-cutting indexes, and L2 method indexes that link to existing source-backed cards. Preserve current top-level handbook files as compatibility indexes until the new structure is validated.

**Tech Stack:** Markdown, YAML, JSONL, PowerShell, Git.

## Global Constraints

- Default L0 loading references no source-card prose.
- Every SOP state has an L1 playbook and checklist.
- Every cross-cutting index maps its concern into lifecycle states.
- Every L2 entry has a stable knowledge-unit ID or an explicit `workflow-native` rationale.
- Do not delete registry or source packs.
- Keep all links relative and validate them.

---

### Task 1: Add L0 Router and Manifest

**Files:**
- Create: `workflow-b/manifest.yaml`
- Create: `workflow-b/L0/router.md`
- Create: `workflow-b/L0/principles.md`
- Create: `workflow-b/L0/project-profiles.md`
- Create: `workflow-b/L0/sop-state-machine.md`
- Modify: `workflow-b/README.md`

**Interfaces:**
- Consumes: existing `workflow-b/principles.md`, `project-profiles.md`, `sop-state-machine.md`.
- Produces: the default runtime entry point and state/cross-cutting loading map.

- [ ] Copy concise authoritative L0 content and add explicit load order.
- [ ] Define manifest triggers for requirements, architecture, high concurrency, security, reliability, performance, consistency, and observability.
- [ ] Make the README point to L0 and state that registry/source data is provenance, not default context.

### Task 2: Create L1 State Playbooks and Checklists

**Files:**
- Create: `workflow-b/states/problem-framing/playbook.md`
- Create: `workflow-b/states/problem-framing/checklist.md`
- Create: `workflow-b/states/requirements/playbook.md`
- Create: `workflow-b/states/requirements/checklist.md`
- Create: `workflow-b/states/architecture/playbook.md`
- Create: `workflow-b/states/architecture/checklist.md`
- Create: `workflow-b/states/construction/playbook.md`
- Create: `workflow-b/states/construction/checklist.md`
- Create: `workflow-b/states/verification/playbook.md`
- Create: `workflow-b/states/verification/checklist.md`
- Create: `workflow-b/states/release/playbook.md`
- Create: `workflow-b/states/release/checklist.md`
- Create: `workflow-b/states/operations/playbook.md`
- Create: `workflow-b/states/operations/checklist.md`

**Interfaces:**
- Consumes: L0 state contracts and existing handbook entries.
- Produces: concise state-level guidance with entry, activity, output, exit, gate, fallback, and next-load fields.

- [ ] Write one playbook per SOP state without embedding full source-card prose.
- [ ] Write evidence-oriented checklists for each state.
- [ ] Link each state to its methods index and relevant cross-cutting indexes.

### Task 3: Add Cross-Cutting Indexes

**Files:**
- Create: `workflow-b/cross-cutting/security/index.md`
- Create: `workflow-b/cross-cutting/reliability/index.md`
- Create: `workflow-b/cross-cutting/performance/index.md`
- Create: `workflow-b/cross-cutting/consistency/index.md`
- Create: `workflow-b/cross-cutting/observability/index.md`
- Create: `workflow-b/cross-cutting/data-and-privacy/index.md`

**Interfaces:**
- Consumes: existing knowledge-unit IDs for security, Release It!, architecture quality, requirements, and oneCoupon constraints.
- Produces: state-by-state projection tables and L2 links.

- [ ] For each concern, define requirements, architecture, construction, verification, release, and operations questions.
- [ ] Include high-concurrency routing for performance, consistency, reliability, and observability.
- [ ] Keep indexes concise and defer detailed procedures to L2.

### Task 4: Create L2 Method Indexes and Templates

**Files:**
- Create: `workflow-b/states/*/methods-index.md`
- Create: `workflow-b/L2/methods/README.md`
- Create: `workflow-b/L2/patterns/README.md`
- Create: `workflow-b/L2/test-strategies/README.md`
- Modify: `workflow-b/templates/*.md`

**Interfaces:**
- Consumes: `registry/knowledge-units.jsonl` and source-card paths.
- Produces: method indexes that route to detailed cards/templates without forcing them into L0/L1.

- [ ] Group existing knowledge units by state and concern.
- [ ] Add applicability and loading notes to each index.
- [ ] Link requirement, design decision, release, and test templates from relevant state indexes.

### Task 5: Add L3 Provenance Guide and Compatibility Links

**Files:**
- Create: `workflow-b/L3/provenance-guide.md`
- Modify: `workflow-b/handbook/*.md`

**Interfaces:**
- Consumes: `registry/`, `sources/`, and existing handbook links.
- Produces: explicit explanation of how L2 IDs resolve to source evidence.

- [ ] Document the path `L2 method → KU ID → source card → source locator`.
- [ ] Keep existing handbook files as compatibility indexes and link them to the new state/cross-cutting indexes.
- [ ] Mark source evidence as on-demand rather than default reading.

### Task 6: Validate Progressive Disclosure

**Files:**
- Create: `tools/validate_handbook_visibility.py`
- Create: `reports/handbook-visibility-validation.md`

**Interfaces:**
- Consumes: manifest, L0-L3 files, links, and registry IDs.
- Produces: validation report and nonzero exit on broken required structure or links.

- [ ] Validate manifest paths exist.
- [ ] Validate every SOP state has playbook, checklist, and methods index.
- [ ] Validate every L2 knowledge-unit reference exists in the registry.
- [ ] Validate relative Markdown links resolve.
- [ ] Verify three loading scenarios: requirements, architecture, and high-concurrency reliability.

