# Design Readiness Checklist

Check each item with evidence; do not use percentage-complete as a substitute.

- [ ] Evidence register classifies material claims and construction-blocking unknowns are resolved by an accountable human.
- [ ] The document set has one canonical Product/Requirements, Technical Design, Verification/Acceptance, and risk-triggered Operations/SLO primary document.
- [ ] Every primary document identifies its readers, decisions, scope, status, owner, change summary, evidence, and next action.
- [ ] Requirements have concrete acceptance scenarios and risk-triggered analysis models.
- [ ] Each selected architecture view has an intended use, primary representation, catalog, semantics, rationale, and mapping.
- [ ] Interfaces, data ownership/constraints, concurrency/failure behavior, and recovery meet the triggered detail contract.
- [ ] arc42 navigates the detailed evidence package without duplicating or hiding it.
- [ ] Active reviewers can answer their intended questions; findings have owners and dispositions.
- [ ] Package status is `READY_FOR_HUMAN_REVIEW`; construction requires separate human acceptance.
- [ ] Run `scripts/validate_project_design_package.py <design-package-path>` with no errors.

## Gates
- [ ] Requirements-to-acceptance review
- [ ] Architecture/contract review
- [ ] Consistency and recovery review
- [ ] Test strategy review
