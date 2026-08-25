# Document Product Architecture

Use this contract when a project needs documents that will be read by people, reviewed as decisions, or used to implement and operate a system. The goal is a coherent document product, not a larger folder of reports.

## Core Model

Every project uses four document classes. Each class has one canonical primary document; supporting evidence may be split into focused files and linked back to the primary document.

| Class | Canonical primary document | Primary readers | Answers |
|---|---|---|---|
| Product and requirements | Product/requirements specification | Product owner, users, developers, testers | Why build it, for whom, what behavior is required, what is out of scope, and how success is recognized. |
| Technical design | Technical design document | Architect, developers, reviewers, operators | Which structure and decisions implement the requirements, what alternatives were rejected, and how normal/failure behavior works. |
| Verification and delivery | Verification and acceptance plan | Testers, developers, release owner | What will be checked, with which oracle, in which environment, and what permits the increment to ship. |
| Operations and reliability | Operations/SLO document | Operators, SRE, product owner, incident responders | What reliability means, how it is measured, how overload/failure is handled, and what action follows a breach. |

`arc42.md` is a navigation view within the Technical Design class. It is not a replacement for the Product/Requirements Specification or the detailed Technical Design document.

A PDF compendium or single-file export is a derived distribution artifact. It must be generated from the canonical primary documents, may be committed for reader convenience, and must not become a second editable source of truth.

## Document Header Contract

Every canonical primary document begins with:

| Field | Requirement |
|---|---|
| Status | `DRAFT`, `IN_REVIEW`, `BASELINED`, `SUPERSEDED`, or `REWORK_REQUIRED`. |
| Version | Stable version and baseline/increment identifier. |
| Owner | One accountable human role. |
| Readers | Named roles and the decisions/tasks they use the document for. |
| Scope | What the document covers and explicitly does not cover. |
| Change summary | What changed since the previous baseline and why. |
| Decision summary | Decisions made, decisions pending, and who can decide. |
| Evidence summary | Sources, experiments, observations, and known limitations. |
| Next action | The next state, owner, and exit evidence. |

## Main Narrative Rule

The primary document must be understandable in one continuous read by its intended audience. Tables, ADRs, diagrams, and evidence files support the narrative; they must not force the reader to reconstruct the project's story from IDs alone.

The primary document must contain:

1. A short executive summary and scope boundary.
2. A coherent end-to-end scenario or architecture narrative.
3. The key decisions and trade-offs in context.
4. Links to focused detail where implementation or verification needs precision.
5. A current status and explicit unresolved items.

## Evidence and Decision Separation

Keep these distinct:

- A product fact is evidence-backed business behavior.
- A requirement is a baseline statement derived from accepted product facts.
- An architecture decision is a response to a requirement/quality driver.
- An implementation detail is a construction choice constrained by the design.
- A verification result is evidence that a built artifact met a requirement.

Do not put an implementation choice in the requirements primary document merely because it appears in the reference system. Do not put an unresolved product question in an ADR and call it a decision.

## Review Record Contract

Use a review record with findings, not a completed checklist alone:

| Finding | Evidence | Impact | Severity | Owner | Disposition | Closure evidence |
|---|---|---|---|---|---|---|

The reviewer asks whether the document answers the intended reader's questions. `READY_FOR_HUMAN_REVIEW` means the agent has assembled evidence and identified decisions; it is not approval. Human acceptance must name the accepted baseline, risks, and next state.

## Change and Baseline Rules

- Keep one canonical version for each document class.
- Record a changelog entry for scope, behavior, quality target, interface, state, or decision changes.
- A change to a requirement must show affected design, acceptance, release, and operations impact.
- A change to a design decision must show affected requirements and verification impact.
- Do not duplicate normative text across documents. Link to the authority and summarize the consequence.
- A project may use a light document set, but must explain which canonical questions are answered by which artifact.

## Quality Review Questions

- Can a product owner explain the user outcome without reading architecture details?
- Can a developer identify the component, data fact, interface, failure behavior, and test oracle without guessing?
- Can a tester identify setup, stimulus, expected response, durable facts, prohibited facts, and observation method?
- Can an operator identify SLO/SLI, alerts, overload behavior, recovery action, and escalation owner?
- Can a reviewer identify what changed, why, who accepted it, and what remains unresolved?

## External Comparators

- Google Cloud API Design Guide: a living, normative guide with explicit requirement keywords and changelog.
- Google SRE Workbook, “Implementing SLOs”: reliability targets are decision tools, not descriptive prose.
- AWS Well-Architected Framework: constructive review questions plus remediation, not a document-completeness audit.
- Microsoft Azure Architecture Center: architecture styles explain when to choose, benefits, challenges, practices, and deployment.
- Google Engineering Practices: technical facts and data should overrule preference; review findings need an owner and resolution path.
