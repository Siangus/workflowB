---
name: workflow-b
description: Guide software engineering work from problem framing through requirements, architecture, implementation, verification, release, and feedback using progressive loading. Use for designing, building, reviewing, or validating a software project when disciplined lifecycle decisions, quality attributes, and traceability matter.
metadata:
  short-description: Progressive software engineering handbook and SOP
---

# Workflow B

Use this skill as the engineering control plane for a project. It provides routes, state playbooks, cross-cutting concerns, methods, templates, and on-demand evidence.

## Start Here

1. Read `manifest.yaml`.
2. Read the four default L0 files:
   - `L0/router.md`
   - `L0/principles.md`
   - `L0/project-profiles.md`
   - `L0/sop-state-machine.md`
3. Identify the project profile and current SOP state.
4. Read only the matching L1 state files listed in the manifest.
5. Enable cross-cutting modules only when the profile or risk triggers them.
6. Before baselining requirements or declaring a design package ready, read `L2/quality-contracts/evidence-and-implementation-detail.md`.
7. Before creating or reviewing project documents, read `L2/quality-contracts/document-product-architecture.md`.
8. Read one L2 method or template only when its concrete activity is selected.
9. Read L3 provenance only for traceability, conflict resolution, audit, or deep study.

## Loading Contract

```text
L0: route and decide
L1: execute the current state
L2: perform a method or use a template
L3: inspect source-backed evidence
```

Do not load the entire handbook by default. Do not substitute a technical mechanism for a business requirement. Do not call an increment complete until the active state's exit evidence and quality gates are met.

Before entering `construction`, the project must pass the `design-readiness` state and produce the risk-appropriate project design package in `templates/project-design-package/`, including the required `arc42.md`. Run `scripts/validate_project_design_package.py <design-package-path>` as a structural check; it cannot approve content. An agent may only recommend `READY_FOR_HUMAN_REVIEW`. Architecture discussion alone is not sufficient evidence.

## Project Profiles

- Use `Exploratory Iterative` for uncertain product work with short feedback cycles.
- Use `Complex Domain` when business language and rules require explicit domain boundaries.
- Use `High Assurance` when safety, regulation, contracts, auditability, or failure cost is high.
- Use `Distributed High Concurrency` for traffic spikes, shared state, asynchronous messages, or multi-node failures.
- Use `Legacy Evolution` for modification of existing systems with implicit rules or incomplete tests.

Profiles may combine. A high-concurrency coupon system normally enables performance, consistency, reliability, and observability.

## Required Engineering Rules

- Record a requirement as a measurable behavior, constraint, or quality scenario, not as a preferred technology.
- Return success only when the business fact claimed by the response is durable and queryable.
- Preserve decision ownership, configuration identity, change communication, and acceptance evidence.
- Use the smallest artifact and process weight that meets the project risk.
- Produce one canonical primary document per document class; use supporting artifacts to provide evidence, not competing narratives.
- Make every primary document useful to a named reader in one continuous read, with status, owner, change summary, decisions, evidence, and next action.
- When requirements, architecture, implementation, or verification invalidate an assumption, follow the active state's fallback rather than hiding the failure.

## References

- State playbooks and checklists: `states/`
- Cross-cutting modules: `cross-cutting/`
- Detailed source-backed methods: `L2/methods/`
- Reusable templates: `templates/`
- Evidence and implementation-detail contract: `L2/quality-contracts/`
- Document product architecture contract: `L2/quality-contracts/document-product-architecture.md`
- Provenance, conflicts, and knowledge registry: `L3/` and `references/provenance/`
