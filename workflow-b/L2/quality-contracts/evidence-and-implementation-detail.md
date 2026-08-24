# Evidence and Implementation-Detail Contract

Use this contract when preparing requirements, architecture, or a project design package. It is a quality contract, not a request to produce a fixed number of files.

## Governing Rule

A document is ready only when its intended reader can answer the decisions needed for the next state without inventing missing business facts, technical behavior, or verification criteria. A heading, diagram, ID, or completed checkbox is not evidence of that capability.

An agent may synthesize, organize, challenge, and propose. It must not silently promote an inference, a guessed threshold, or a preferred technology to a confirmed business fact. It may mark a package `DRAFT` or `READY_FOR_HUMAN_REVIEW`; only an accountable human can accept scope, business rules, quality trade-offs, or residual risk.

## Claim Classes

Record every material statement in the evidence register before it becomes a baseline requirement or architecture driver.

| Class | Meaning | Minimum record | May enter a baseline? |
|---|---|---|---|
| Confirmed fact | A stakeholder, source system, contract, policy, or observed behavior supports the claim. | Source type, locator or meeting record, date, and accountable owner. | Yes. |
| Derived interpretation | A conclusion drawn from one or more confirmed facts. | Links to supporting evidence and explicit reasoning. | Only after owner review. |
| Proposal | A candidate requirement, design, experiment, or option. | Rationale, alternatives when material, and decision owner. | No until decided. |
| Assumption | A working belief without adequate support. | Impact if false, validation method, owner, and deadline. | Only as a labeled experiment constraint. |
| Open question | Information required to decide. | Decision owner, blocking level, and needed-by point. | No. |

Never use a source book or a reference implementation as evidence that a product owner wants a feature. They may justify a method or reveal a technical option, but product facts require product evidence.

## Requirement Detail Contract

For every in-scope requirement, a product owner, developer, and tester must be able to answer all applicable questions:

| Question | Required detail |
|---|---|
| Why does it exist? | Linked business objective and evidence IDs; owner and priority. |
| Who and when? | Actor, trigger, preconditions, authorization/ownership context, and time boundary. |
| What changes? | Observable behavior, business data/state before and after, and invariant/rule IDs. |
| What if it cannot proceed? | Named alternate, exception, cancellation, duplicate, and invalid-input behavior where relevant. |
| What is deliberately absent? | Scope boundary and linked non-goal. |
| How is it accepted? | At least one concrete acceptance scenario with setup, action, expected response, expected durable/observable facts, and observation method. |

One requirement must express one behavior or constraint. Cross-cutting rules remain atomic in the business-rule catalog and are referenced, not copied. A quality requirement additionally names stimulus source, environment, response, measure, threshold or explicitly unresolved decision, priority, and validation method.

## Design Detail Contract

Design describes a response to a driver, not a technology preference. Each selected design item must identify the driver/evidence, options considered when the decision is consequential, chosen response, consequences, validation, owner, and unresolved risk.

Use only views with a named stakeholder question. Every view must contain a primary representation plus an element/relation catalog, relation semantics, constraints, rationale, and mappings to related views. `arc42.md` is the navigation narrative; it is not a substitute for these view specifications.

| Trigger | Required implementation-facing detail |
|---|---|
| Stateful rule, lifecycle, or multiple actors | Ubiquitous-language terms, command/event or scenario model, state transitions, rule priority, and exception paths. |
| External, service, database, message, or file interface | Consumer/provider, schema or field dictionary, preconditions, postconditions/effects, errors, ordering, timeouts, authentication, examples, evolution policy, and contract verification. |
| Durable data or retained business fact | Ownership, data dictionary, identity, cardinality, constraints/indexes, retention, migration/compatibility, and authoritative-query rule. |
| Concurrent writes or distributed business effect | Business transaction boundary, invariant, isolation/lock or conditional-update policy, contention trace, conflict classification, retry/idempotency semantics, timeout/partial-failure recovery, and contention test design. |
| Quality attribute is architecturally significant | Ranked quality scenario, tactic/decision link, sensitivity/trade-off, capacity or failure assumption, and validation experiment or test. Unknown threshold is an open decision, not a fabricated number. |
| Multiple deployable units or runtime variants | Context/integration map, ownership and change policy, runtime behavior for normal and failure paths, deployment/configuration mapping, and operational observability. |

## Acceptance Scenario Contract

An acceptance scenario is not a test ID. Each scenario records:

1. Evidence and requirement/rule references.
2. Initial data, configuration, identities, clock, and dependency state.
3. A concrete command or external stimulus.
4. Expected response and externally visible side effects.
5. Expected durable facts, prohibited facts, and how each is observed.
6. For concurrent or failure scenarios: participants, schedule/fault injection, completion bound if known, and invariant oracle.

Executable automation may be linked later, but the scenario must be understandable and reviewable before code exists.

## Active Review

Reviewers do not ask whether a document exists. They sample high-risk requirements and scenarios and try to answer:

- Product reviewer: Which source or decision established this rule? What business result changes if it is false?
- Implementer: What exact state/data change, transaction boundary, failure result, and interface semantics must I implement?
- Tester: What initial conditions, action, observable oracle, and prohibited outcome prove this?
- Interface consumer: Can I call this interface and recover from each documented error without reading the provider code?
- Architect: Which driver chose this structure over alternatives, and which scenario could invalidate it?

An unanswered question creates a finding with owner, affected artifact, blocking level, and resolution path. A human review record must distinguish confirmed findings, accepted risks, and work still open.

## Provenance

- `KU-0028`, `KU-0030`–`KU-0034`, `KU-0037`, `KU-0041`: business objectives, elicitation, requirement quality, models, quality measures, validation, and traceability.
- `KU-0015`, `KU-0017`–`KU-0021`: bounded contexts, integration ownership, invariants, events, and domain discovery.
- `KU-0043`, `KU-0044`, `KU-0052`–`KU-0054`: quality-driven architecture, iterative design, scenario analysis, trade-offs, and evidence.
- `KU-0055`–`KU-0062`: view selection, element catalogs, interface/behavior documentation, dynamism, and active review.
- `KU-0065`, `KU-0067`: relational persistence and concurrency/transaction design.

Read the cited L2 methods or L3 provenance when a concrete activity needs source detail.
