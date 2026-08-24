# Design Readiness Playbook

**Goal:** Assemble and review the project design package before construction.

**Entry:** Requirements and architecture outputs exist for the proposed V1 slice.

## Activities
1. Create the project design package and use `arc42.md` as its architecture index.
2. Define state, rules, quality scenarios, views, data/recovery, interfaces, ADRs, tests, and traceability.
3. Review evidence and record the readiness decision.

## Outputs
- Project design package
- arc42 architecture document
- Design-readiness review
- Approved risks or rework findings

## Exit Evidence
- Required design-package artifacts exist.
- Critical requirements trace to design and tests.
- arc42 describes context, constraints, strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality, risks, and glossary.
- Review decision is APPROVED or APPROVED_WITH_RISKS.

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
- `cross-cutting/security/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
- `cross-cutting/data-and-privacy/index.md`
