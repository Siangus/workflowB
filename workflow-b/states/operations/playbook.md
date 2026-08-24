# Operate and Learn Playbook

**Goal:** Observe live outcomes, control failure impact, and feed evidence back into engineering decisions.

**Entry:** Release is accepted and operational ownership exists.

## Activities
1. Observe demand, defects, reliability, cost, and change impact.
2. Capture incidents and user feedback.
3. Use bounded controls, recovery, and safe operational actions.
4. Feed evidence into requirements, risks, architecture debt, and planning.

## Outputs
- Operational observations
- Incident records
- Improvement backlog
- Updated risk/value decisions

## Exit Evidence
- Signals reach accountable owners.
- Recovery behavior is tested or rehearsed.
- Learning produces an owned follow-up decision.

## Quality Gates
- Operational review
- Feedback-to-backlog audit
- Recovery evidence review

**Fallback:** Escalate systemic instability to planning and risk management.
**Next state:** `plan-and-commit`

## Load Next
- `states/operations/checklist.md`
- `states/operations/methods-index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
- `cross-cutting/security/index.md`
- `cross-cutting/performance/index.md`
