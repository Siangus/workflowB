# Release Readiness Playbook

**Goal:** Make a verified increment deployable, compatible, recoverable, and auditable.

**Entry:** Verification exit criteria are met.

## Activities
1. Verify artifact, configuration, schema, and interface identity.
2. Run deployment and smoke checks.
3. Validate migration compatibility and rollback/roll-forward.
4. Obtain the accountable release decision.

## Outputs
- Release candidate
- Approval record
- Deployment evidence
- Rollback plan
- Compatibility record

## Exit Evidence
- Build and configuration identity are verified.
- Monitoring and recovery are ready.
- Approval is complete.
- Known compatibility risks are accepted or resolved.

## Quality Gates
- Release checklist
- Deployment/rollback check
- Compatibility check
- Security/audit check

**Fallback:** Return to verification or construction when release evidence fails; use rollback or roll-forward according to the compatibility plan.
**Next state:** `operations`

## Load Next
- `states/release/checklist.md`
- `states/release/methods-index.md`
- `cross-cutting/security/index.md`
- `cross-cutting/reliability/index.md`
- `cross-cutting/observability/index.md`
- `cross-cutting/data-and-privacy/index.md`
- `cross-cutting/consistency/index.md`
