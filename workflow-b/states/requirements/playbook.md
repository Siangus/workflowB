# Discovery and Requirements Playbook

**Goal:** Create an evidence-backed, reviewable near-term requirement set with enough behavioral detail for design and acceptance work.

**Entry:** A problem frame and stakeholder plan exist.

## Activities
1. Build the evidence register; distinguish confirmed facts, interpretations, proposals, assumptions, and open questions.
2. Elicit scenarios, rules, data, quality attributes, interfaces, and exceptions from the relevant stakeholder or source.
3. Create requirement cards, rule catalog entries, models, and acceptance scenarios when prose cannot answer a reader's questions.
4. Use models, prototypes, or spikes to reduce uncertainty; do not convert uncertainty into invented requirements.
5. Prioritize and validate the selected scope with product, development, and test representatives.
6. Choose baseline or just-in-time elaboration according to profile.

## Outputs
- Evidence register and unresolved-decision register
- Requirement cards or stories with source, rationale, and verification information
- Concrete acceptance scenarios
- Business-rule catalog
- Models, prototype findings, and decision records

## Exit Evidence
- Each baseline claim has evidence or an accountable human decision.
- Near-term requirements and acceptance scenarios are specific enough that a tester can derive an oracle without guessing.
- Priority owner agrees on the work set.
- Relevant users, engineers, and testers have walked through high-risk behavior.
- Quality attributes have measurable scenarios.

## Quality Gates
- Completeness and testability review
- Quality-attribute scenario review
- Stakeholder confirmation
- Evidence and assumption review

**Fallback:** Return to problem framing when value or scope is unstable; create a prototype or spike for unresolved uncertainty.
**Next state:** `architecture`

## Load Next
- `states/requirements/checklist.md`
- `states/requirements/methods-index.md`
- `L2/quality-contracts/evidence-and-implementation-detail.md`
- `cross-cutting/security/index.md`
- `cross-cutting/data-and-privacy/index.md`
- `cross-cutting/performance/index.md`
- `cross-cutting/consistency/index.md`
- `cross-cutting/reliability/index.md`
