# SOP State Machine

Each state is a control-plane contract; handbook links hold execution detail.

## Problem Framing
- **state_id:** `problem-framing`
- **goal:** Establish a measurable business problem, scope boundary, and decision mandate.
- **entry_criteria:** Accountable sponsor and opportunity exist.
- **activities:** Define business problem, vision, scope, exclusions, stakeholders, subdomains, success measures, and top risks.
- **outputs:** Vision and scope; Stakeholder map; Success measures; Proceed/pivot/prototype decision
- **exit_criteria:** Success measures are observable.; Scope boundary and decision owner are explicit.; Top risks have owners.
- **quality_gates:** Review vision, scope, and risk assumptions.
- **roles:** Product owner; Business sponsor; Lead engineer
- **fallback:** Return when new evidence invalidates value, scope, or domain assumptions.
- **next_state:** `discovery-and-requirements`
- **handbook:** `handbook/management.md`

## Discovery and Requirements
- **state_id:** `discovery-and-requirements`
- **goal:** Create testable, owned, prioritized near-term requirements with appropriate detail.
- **entry_criteria:** Problem frame and stakeholder plan exist.
- **activities:** Elicit scenarios, rules, data, quality attributes, interfaces, exceptions, and acceptance criteria.; Use models or prototypes to reduce uncertainty.; Prioritize and validate the selected scope.
- **outputs:** Requirements or stories; Acceptance criteria; Models/prototype findings; Open issue register
- **exit_criteria:** Near-term requirements are testable.; Priority owner agrees on the work set.; Key users, engineers, and testers share understanding.
- **quality_gates:** Requirements completeness and testability review.; Quality-attribute scenario review.
- **roles:** Business analyst; Product owner; Domain expert; Engineer; Tester
- **fallback:** Return to problem framing when value or scope is unstable.
- **next_state:** `architecture-and-domain-design`
- **handbook:** `handbook/requirements.md`

## Architecture and Domain Design
- **state_id:** `architecture-and-domain-design`
- **goal:** Select boundaries, quality tactics, integration contracts, and implementation patterns that support the next value slice.
- **entry_criteria:** Testable scope slice and architecturally significant requirements are known.
- **activities:** Define quality attribute scenarios.; Choose module, component-and-connector, and allocation views.; Apply Attribute-Driven Design.; Select domain, data, concurrency, presentation, and distribution patterns only when justified.; Document interfaces, behavior, rationale, mappings, and debt.; Evaluate the architecture with a focused review or ATAM-style method.
- **outputs:** Quality attribute scenarios; Architecture decision record; Selected views and mappings; Interface/behavior contracts; Pattern decision; Evaluation findings; Architecture debt items
- **exit_criteria:** Architecture drivers have design responses.; Boundaries and ownership are reviewable.; Interfaces and behavior are testable.; Major trade-offs and risks are recorded.; Documentation is usable by intended stakeholders.
- **quality_gates:** Quality scenario review.; Architecture and contract review.; View/documentation completeness review.; Aggregate/concurrency review where applicable.; Architecture risk evaluation.
- **roles:** Architect/lead engineer; Domain expert; Product owner; Reviewer; Tester
- **fallback:** Return to discovery when requirements or quality scenarios conflict; create a spike when the architecture risk is not understood.
- **next_state:** `plan-and-commit`
- **handbook:** `handbook/design.md`

## Plan and Commit
- **state_id:** `plan-and-commit`
- **goal:** Select a feasible, value-bearing work set and make scope trade-offs explicit.
- **entry_criteria:** Prioritized backlog or approved baseline exists.; Dependencies and material risks are visible.
- **activities:** Select value slices.; Assess capacity, risks, dependencies, and changes.; Record commitments and deferred scope.; Use rolling planning or formal estimation according to profile.
- **outputs:** Iteration/release plan; Risk updates; Commitment decision; Deferred-scope list
- **exit_criteria:** Work set fits capacity and constraints.; High risks have responses and triggers.; Deferred work has an explicit rationale.
- **quality_gates:** Capacity and risk review.; Baseline/change authorization where required.
- **roles:** Product owner; Project lead; Delivery team; Risk owner
- **fallback:** Reprioritize or renegotiate scope, date, resources, or quality; never hide the trade-off.
- **next_state:** `construct-and-integrate`
- **handbook:** `handbook/management.md`

## Construct and Integrate
- **state_id:** `construct-and-integrate`
- **goal:** Implement a maintainable, integrated vertical increment under configuration control.
- **entry_criteria:** The next slice has acceptance evidence and needed design decisions.
- **activities:** Implement the vertical slice.; Run developer checks.; Review and integrate frequently.; Publish events safely when required.; Maintain configuration identity.
- **outputs:** Integrated build; Code/review evidence; Automated developer checks; Updated configuration record
- **exit_criteria:** Integrated build is green.; Changes have review and test evidence.; No unexplained contract break exists.
- **quality_gates:** CI and regression checks.; Configuration and contract checks.
- **roles:** Engineer; Reviewer; Release engineer
- **fallback:** Return to design or requirements when the slice exposes an invalid assumption.
- **next_state:** `verify-and-release`
- **handbook:** `handbook/construction.md`

## Verify and Release
- **state_id:** `verify-and-release`
- **goal:** Demonstrate protected behavior and decide whether the increment is safe to release.
- **entry_criteria:** Potentially shippable integrated increment exists.
- **activities:** Run acceptance, regression, load, security, recovery, and failure-mode checks as applicable.; Validate traceability and release evidence.; Verify deployment artifact, configuration, health signals, and rollback.; Obtain release decision.
- **outputs:** Test results; Release candidate; Traceability/release evidence; Rollback plan; Release decision
- **exit_criteria:** Protected behavior passes.; Known risk is dispositioned.; Release has accountable approval or rejection.
- **quality_gates:** Acceptance and regression review.; Stability and failure-mode review.; Security, performance, recovery, and audit checks as applicable.; Deployment/rollback readiness check.
- **roles:** Tester; Engineer; Risk owner; Release approver
- **fallback:** Return to construction, design, discovery, or planning based on the defect origin.
- **next_state:** `operate-and-learn`
- **handbook:** `handbook/testing.md`

## Operate and Learn
- **state_id:** `operate-and-learn`
- **goal:** Observe live outcomes and turn evidence into owned improvement decisions.
- **entry_criteria:** Release is accepted.
- **activities:** Observe demand, defects, reliability, cost, and change impact.; Capture incidents and user feedback.; Feed learning into value, requirements, risks, and backlog.
- **outputs:** Operational observations; Incident records; Improvement backlog; Updated risk/value decisions
- **exit_criteria:** Signals reach accountable owners.; Learning produces a follow-up decision or an explicit no-action rationale.
- **quality_gates:** Operational review and feedback-to-backlog audit.
- **roles:** Operations; Product owner; Engineer; Risk owner
- **fallback:** Escalate systemic instability to planning and risk management.
- **next_state:** `plan-and-commit`
- **handbook:** `handbook/operations.md`
