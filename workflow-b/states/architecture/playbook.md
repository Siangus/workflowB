# Architecture and Domain Design Playbook

**Goal:** Select and explain boundaries, quality responses, interfaces, and implementation constraints for the next value slice.

**Entry:** Testable scope and architecturally significant requirements are known.

## Activities
1. Select architecturally significant requirements and quality scenarios with their evidence and priority.
2. Choose only the views required by stakeholder decisions; specify each view's elements, relations, semantics, catalog, and rationale.
3. Apply incremental architecture design and record alternatives for consequential choices.
4. Define domain boundaries, data ownership, consistency/invariant boundaries, and integration/change relationships where applicable.
5. Specify interfaces and high-risk behavior well enough for consumers, implementers, and testers to work independently.
6. For concurrency, failure, or distributed effects, define the business transaction, contention/failure traces, recovery, and verification oracle.
7. Evaluate high-risk scenarios with stakeholders; record risks, sensitivity points, trade-offs, and needed experiments.

## Outputs
- Quality attribute scenarios
- Technical Design Document as the canonical primary document
- Architecture decision records with alternatives and validation
- View catalog, views, element/relation catalogs, and mappings
- Interface and behavior contracts
- Data ownership, consistency, and recovery design when triggered
- Evaluation findings and architecture debt items

## Exit Evidence
- Architecture drivers have evidence-backed design responses and validation plans.
- Boundaries, ownership, invariants, and integration/change policies are reviewable.
- Interfaces and high-risk behaviors specify normal, error, timeout, and ordering semantics.
- Major trade-offs, sensitivity points, assumptions, and risks are recorded with owners.
- Intended stakeholders can use the documentation to answer their implementation or review questions.
- The Technical Design Document presents one coherent end-to-end design before linking to focused views, ADRs, contracts, and data details.

## Quality Gates
- Quality scenario review
- Architecture and contract review
- View/documentation completeness review
- Concurrency/invariant review
- Architecture risk evaluation

**Fallback:** Return to requirements when quality scenarios or language conflict; create a spike when architecture risk is not understood.
**Next state:** `design-readiness`

## Load Next
- `states/architecture/checklist.md`
- `states/architecture/methods-index.md`
- `L2/quality-contracts/evidence-and-implementation-detail.md`
- `cross-cutting/security/index.md`
- `cross-cutting/data-and-privacy/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
