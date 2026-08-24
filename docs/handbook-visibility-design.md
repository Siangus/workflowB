# Workflow B Handbook Visibility Design

## Goal

Restructure Workflow B as a handbooks-first knowledge product with progressive disclosure. Agents should load only the routing and current-state material by default, then load methods, templates, cross-cutting modules, and provenance only when the project context requires them.

## Product Boundary

- Workflow A remains responsible for reading books, extracting knowledge units, and maintaining provenance.
- Workflow B remains the human- and agent-readable engineering handbook and SOP.
- `registry/` and `sources/` are build/provenance data and are not part of the default runtime context.
- This change reorganizes and materializes B; it does not add new source books.

## Visibility Levels

| Level | Contents | Loading policy |
|---|---|---|
| L0 | Router, principles, project profiles, SOP state machine, loading manifest | Always available at workflow entry |
| L1 | State playbooks, state checklists, cross-cutting indexes | Load after selecting the current state/profile |
| L2 | Detailed methods, decision tables, patterns, test strategies, templates | Load only for the current activity or question |
| L3 | Source cards, citations, conflicts, full evidence and historical rationale | Load only for traceability, disagreement, audit, or deep study |

## Directory Contract

```text
workflow-b/
  manifest.yaml
  README.md
  L0/
    router.md
    principles.md
    project-profiles.md
    sop-state-machine.md
  states/
    problem-framing/
      playbook.md
      checklist.md
      methods-index.md
    requirements/
      playbook.md
      checklist.md
      methods-index.md
    architecture/
      playbook.md
      checklist.md
      methods-index.md
    construction/
      playbook.md
      checklist.md
      methods-index.md
    verification/
      playbook.md
      checklist.md
      methods-index.md
    release/
      playbook.md
      checklist.md
      methods-index.md
    operations/
      playbook.md
      checklist.md
      methods-index.md
  cross-cutting/
    security/
      index.md
    reliability/
      index.md
    performance/
      index.md
    consistency/
      index.md
    observability/
      index.md
    data-and-privacy/
      index.md
  L2/
    methods/
    patterns/
    test-strategies/
  templates/
  L3/
    provenance-guide.md
```

Existing handbook files may remain as compatibility indexes during migration, but L0/L1 must become the authoritative runtime entry points.

## Manifest Contract

`manifest.yaml` must declare:

- default L0 files;
- state-to-playbook and checklist mappings;
- project-profile triggers;
- cross-cutting module triggers;
- L2 method directories;
- L3 provenance locations;
- loading order and maximum default scope.

Example:

```yaml
version: 1
default:
  - L0/router.md
  - L0/principles.md
  - L0/project-profiles.md
  - L0/sop-state-machine.md
states:
  requirements:
    load:
      - states/requirements/playbook.md
      - states/requirements/checklist.md
    methods: states/requirements/methods-index.md
cross_cutting:
  high_concurrency:
    - cross-cutting/performance/index.md
    - cross-cutting/consistency/index.md
    - cross-cutting/reliability/index.md
  regulated:
    - cross-cutting/security/index.md
    - cross-cutting/data-and-privacy/index.md
on_demand:
  methods: L2/methods/
  patterns: L2/patterns/
  templates: templates/
  provenance: L3/
```

## L1 Playbook Contract

Every state playbook must answer:

1. What is the goal of this state?
2. What inputs and entry evidence are required?
3. Who performs the activities?
4. What is the minimum procedure?
5. What artifacts are produced?
6. What evidence permits exit?
7. Which quality gates apply?
8. Which cross-cutting modules should be checked?
9. Where does the workflow return when the state fails?
10. Which L2 methods and templates can be loaded next?

Playbooks should be concise enough to load with the current state. They must not duplicate full source-card prose.

## L1 Checklist Contract

Checklists contain observable yes/no or evidence-required checks. They must not contain unexplained theory. Each check may link to an L2 method or L3 source evidence.

## L2 Method Contract

Each method entry contains:

- trigger and applicability;
- inputs;
- ordered procedure;
- outputs;
- decision points;
- checks;
- failure and fallback behavior;
- tailoring variants;
- related states and cross-cutting modules;
- source knowledge-unit IDs.

## Cross-Cutting Module Contract

Each cross-cutting index describes how the concern projects into states:

| Projection | Required question |
|---|---|
| Requirements | What must the system guarantee? |
| Architecture | Which boundaries, tactics, or contracts provide it? |
| Construction | Which implementation controls must exist? |
| Verification | What evidence proves it? |
| Release | What must be checked before exposure? |
| Operations | What must be observed or recovered? |

Cross-cutting indexes route to L2 methods and do not duplicate every state playbook.

## L3 Provenance Contract

L3 retains source cards, source locators, conflicts, and merge history. L0/L1/L2 references should use stable knowledge-unit IDs instead of embedding long evidence passages.

## Migration Rules

1. Build L0 router and manifest first.
2. Convert each existing state into an L1 playbook and checklist.
3. Convert handbook tables into L2 method indexes and detailed entries.
4. Add cross-cutting indexes for security, reliability, performance, consistency, observability, and data/privacy.
5. Preserve existing links or add compatibility links while moving content.
6. Do not delete registry or source packs during this migration.
7. Validate that every L1/L2 entry has a source or an explicit `workflow-native` rationale.

## Validation Criteria

- Default L0 loading references no source-card prose.
- Every SOP state has an L1 playbook and checklist.
- Every L1 playbook references only relevant L2 entries.
- Every enabled cross-cutting module maps to at least one state.
- Every L2 method has a stable ID and source/provenance reference.
- No broken relative links exist.
- A requirements task, architecture task, and high-concurrency task can be routed without loading unrelated modules.
