# Project Design Package Template

Copy this directory into the project repository before construction. This package is a set of evidence and decision containers, not a fixed report. Keep each artifact only when it answers an actual stakeholder question, but do not omit a risk-triggered artifact. Mark genuinely irrelevant sections as `Not applicable: <reason>`.

`arc42.md` is required as the coherent architecture navigation narrative. It links the detailed evidence; it does not replace it.

## Required Foundation

- `00-charter.md`: problem, scope, decision owner, and success measures.
- `01-requirements-baseline.md`: the selected requirement set, with links to detailed cards/scenarios.
- `evidence-register.md`: claim classification, source/owner, assumptions, and open decisions.
- `02-domain-and-state-model.md`: language, rules, and stateful behavior when the domain is not trivial.
- `03-quality-attribute-scenarios.md`: measurable quality drivers or explicitly unresolved targets.
- `04-architecture-overview.md` and `arc42.md`: navigation into the selected view package.
- `07-api-and-interface-contracts.md`: interface index; detailed contracts must meet the interface detail contract.
- `10-test-and-acceptance-strategy.md`: scenario catalog and verification approach.
- `11-traceability-matrix.md`: links from requirement/rule to evidence, decisions, acceptance scenarios, and later implementation/test evidence.
- `13-design-readiness-review.md`: active-review findings and `READY_FOR_HUMAN_REVIEW` recommendation only.

## Risk-Triggered Detail

Copy and instantiate the matching top-level templates when the selected slice triggers them:

| Trigger | Required detail container |
|---|---|
| Significant workflow, lifecycle, policy, or multi-actor behavior | `requirement-card.md`, `acceptance-scenario.md`, and appropriate state/decision/event models. |
| Durable data, concurrent update, idempotency, or distributed business effect | `data-concurrency-design.md`, runtime/failure traces, and recovery design. |
| Consumer/provider boundary | Detailed interface contracts and one or more `architecture-view.md` documents. |
| Consequential architectural choice or trade-off | `architecture-decision.md` with driver, options, rationale, and validation. |
| Multiple deployables, runtime behavior, or configuration variants | Architecture views plus deployment/configuration and behavior documentation. |

## Gate Semantics

Run `scripts/validate_project_design_package.py <design-package-path>` from the Workflow B Skill directory. It checks navigability and minimum structural relations only; it cannot judge evidence credibility or approve a design. The agent may record `READY_FOR_HUMAN_REVIEW` after an active walkthrough. Construction requires an accountable human acceptance or explicit residual-risk acceptance outside the agent's authority.
