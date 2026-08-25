# Architecture and Domain Design Checklist

Check each item with evidence; do not use percentage-complete as a substitute.

- [ ] Each architecture driver links to evidence, a design response, an owner, and a validation approach.
- [ ] The canonical Technical Design Document has status, owner, readers, scope, change summary, chosen design, alternatives, consequences, risks, validation, and next action.
- [ ] Each selected view has a stakeholder question, primary representation, catalog, relation semantics, rationale, and necessary mapping.
- [ ] Boundaries, ownership, invariants, and integration/change policies are reviewable.
- [ ] Interfaces and high-risk behavior define normal, error, timeout, ordering, and compatibility semantics.
- [ ] Data ownership, durable constraints, and recovery are specified where they affect correctness.
- [ ] Concurrent/distributed paths define transaction boundary, conflict/failure behavior, retry/idempotency semantics, and an invariant oracle.
- [ ] Major trade-offs, sensitivity points, assumptions, and risks are recorded with owners.
- [ ] Intended readers can answer their questions in an active walkthrough.

## Gates
- [ ] Quality scenario review
- [ ] Architecture and contract review
- [ ] View/documentation completeness review
- [ ] Concurrency/invariant review
- [ ] Architecture risk evaluation
