# Verify and Accept Playbook

**Goal:** Demonstrate intended behavior, quality attributes, failure behavior, and acceptance evidence.

**Entry:** A potentially shippable integrated increment exists.

## Activities
1. Run unit, integration, contract, acceptance, and regression checks.
2. Run performance, security, recovery, and failure-mode tests as applicable.
3. Validate traceability and release evidence.
4. Disposition known failures and risks.

## Outputs
- Test results
- Acceptance decision
- Coverage/traceability evidence
- Failure findings
- Release recommendation

## Exit Evidence
- Protected behavior passes.
- Quality targets have evidence.
- Known risks have disposition.
- Acceptance owner approves or rejects explicitly.

## Quality Gates
- Acceptance and regression review
- Quality-attribute review
- Stability/failure review
- Security review where enabled

**Fallback:** Return to construction, architecture, requirements, or planning based on defect origin.
**Next state:** `release`

## Load Next
- `states/verification/checklist.md`
- `states/verification/methods-index.md`
- `cross-cutting/security/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
