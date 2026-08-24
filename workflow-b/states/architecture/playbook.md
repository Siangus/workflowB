# Architecture and Domain Design Playbook

**Goal:** Select boundaries, quality tactics, integration contracts, and implementation patterns for the next value slice.

**Entry:** Testable scope and architecturally significant requirements are known.

## Activities
1. Define quality attribute scenarios.
2. Choose module, runtime, deployment, and behavior views.
3. Apply incremental architecture design.
4. Select domain, data, concurrency, presentation, and distribution patterns only when justified.
5. Document interfaces, rationale, mappings, and debt.
6. Evaluate the architecture against stakeholder risks.

## Outputs
- Quality attribute scenarios
- Architecture decision record
- Selected views and mappings
- Interface/behavior contracts
- Pattern decision
- Evaluation findings
- Architecture debt items

## Exit Evidence
- Architecture drivers have design responses.
- Boundaries and ownership are reviewable.
- Interfaces and behavior are testable.
- Major trade-offs and risks are recorded.
- Documentation is usable by intended stakeholders.

## Quality Gates
- Quality scenario review
- Architecture and contract review
- View/documentation completeness review
- Concurrency/invariant review
- Architecture risk evaluation

**Fallback:** Return to requirements when quality scenarios or language conflict; create a spike when architecture risk is not understood.
**Next state:** `construction`

## Load Next
- `states/architecture/checklist.md`
- `states/architecture/methods-index.md`
- `cross-cutting/security/index.md`
- `cross-cutting/data-and-privacy/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
