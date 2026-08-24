# SOP State Machine

## Problem Framing
`problem-framing` -> `requirements`

Enter with an opportunity or problem and an accountable sponsor. Exit when problem, scope, stakeholders, success evidence, and material risks are explicit. Return when new evidence invalidates the value or scope assumption.

## Requirements Discovery
`requirements` -> `architecture`

Enter with a problem frame. Exit when material claims have evidence or accountable decisions; near-term requirements and acceptance scenarios are owned, prioritized, testable, and walked through by relevant users, engineers, and testers. Return to problem framing when value or scope is unstable.

## Architecture and Domain Design
`architecture` -> `design-readiness`

Enter with testable scope and architecture drivers. Exit when boundaries, quality tactics, interfaces, behavior, data/consistency constraints, rationale, validation, and major risks are reviewable by intended readers. Create a spike or return to requirements when architecture risk is unresolved.

## Design Readiness
`design-readiness` -> `plan-and-commit` -> `construction`

Enter with requirements and architecture outputs. Assemble and actively review the risk-appropriate design package: evidence register, requirement/acceptance scenarios, domain/state model, quality scenarios, views and catalogs, runtime/failure flows, data consistency/recovery, interfaces, decisions, security/risk review, and traceability. The agent can only record `READY_FOR_HUMAN_REVIEW`; construction is blocked until an accountable human accepts the package or explicitly accepts residual risk.

## Plan and Commit
`plan-and-commit` -> `construction`

Select a feasible value-bearing slice, make scope trade-offs explicit, and assign risk responses. Replan or renegotiate when capacity or commitments do not fit.

## Construct and Integrate
`construction` -> `verification`

Implement a vertical slice with tests, review, integration, and configuration identity. Return to architecture or requirements when implementation exposes an invalid assumption.

## Verify and Release
`verification` -> `release` -> `operations`

Verify behavior, quality attributes, security, recovery, compatibility, and release evidence. Release only with an accountable decision and rollback/recovery path.

## Operate and Learn
`operations` -> `plan-and-commit`

Observe outcomes, failures, demand, and cost. Feed evidence into requirements, risks, architecture debt, and planning.
