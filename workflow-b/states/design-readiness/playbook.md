# Design Readiness Playbook

**Goal:** Assemble and actively review an evidence-backed package that allows the selected slice to be implemented and accepted without guessing material behavior.

**Entry:** Requirements and architecture outputs exist for the proposed V1 slice.

## Activities
1. Create the project design package and use `arc42.md` as its architecture navigation narrative.
2. Apply `L2/quality-contracts/evidence-and-implementation-detail.md` to select and elaborate only the artifacts triggered by the slice's risks.
3. Define state, rules, quality scenarios, views, data/recovery, interfaces, decisions, acceptance scenarios, and traceability at the required depth.
4. Conduct an active walkthrough with product, implementation, test, and interface/operations reviewers as relevant.
5. Record findings, blockers, accepted risks, and a `READY_FOR_HUMAN_REVIEW` recommendation. Do not self-approve.

## Outputs
- Project design package
- arc42 architecture navigation document
- Active-review record, findings, and human decision record
- Accepted risks or rework findings

## Exit Evidence
- Material claims are classified in the evidence register; construction-blocking uncertainty is resolved or explicitly rejected by a human owner.
- Critical requirements trace to behavior/design and concrete acceptance scenarios, not only test labels.
- Each risk-triggered design area meets the evidence-and-implementation-detail contract.
- arc42 navigates the views, catalogs, mappings, decisions, quality scenarios, risks, and glossary; it does not replace them.
- Active reviewers can answer their intended questions, and findings have disposition evidence.
- Package status is `READY_FOR_HUMAN_REVIEW`; human acceptance is external to the agent.

## Quality Gates
- Requirements-to-acceptance review
- Architecture/contract review
- Consistency and recovery review
- Test strategy review

**Fallback:** REWORK_REQUIRED returns to requirements or architecture. Construction remains blocked.
**Next state:** `plan-and-commit`

## Load Next
- `states/design-readiness/checklist.md`
- `states/design-readiness/methods-index.md`
- `L2/quality-contracts/evidence-and-implementation-detail.md`
- `cross-cutting/security/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
- `cross-cutting/data-and-privacy/index.md`
