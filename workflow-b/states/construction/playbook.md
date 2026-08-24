# Construct and Integrate Playbook

**Goal:** Implement a maintainable, tested, integrated vertical increment under configuration control.

**Entry:** The next slice has acceptance evidence and required design decisions.

## Activities
1. Implement the smallest vertical slice.
2. Run developer checks and focused integration tests.
3. Review and integrate frequently.
4. Apply transactions, idempotency, timeouts, and boundaries from the architecture.
5. Update configuration and interface identity.

## Outputs
- Integrated build
- Code/review evidence
- Automated developer checks
- Updated configuration record
- Updated traceability

## Exit Evidence
- Integrated build is green.
- Changes have review and test evidence.
- No unexplained contract break exists.
- The slice is demonstrable and potentially releasable.

## Quality Gates
- CI and regression checks
- Code/design review
- Configuration and contract checks

**Fallback:** Return to architecture or requirements when the slice exposes an invalid assumption; record new debt rather than hiding it.
**Next state:** `verification`

## Load Next
- `states/construction/checklist.md`
- `states/construction/methods-index.md`
- `cross-cutting/security/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
