# Tailoring Rules

| Concern | Exploratory iteration | Complex domain | Contractual/high-assurance | Invariant |
|---|---|---|---|---|
| Vision and scope | One-page vision plus near-term stories | Vision plus core-domain rationale | Approved vision/scope and success measures | Every feature has a business rationale |
| Requirements | Stories, examples, acceptance criteria | Ubiquitous language and scenario models | Baselined SRS/RM repository | Requirements are testable |
| Change | Product-owner decision with impact note | Context-map and contract impact review | CCB or delegated authority | Impact and decision are recorded |
| Design | Enough design for next vertical slice | Bounded contexts, aggregates, event contracts | Reviewed architecture and quality scenarios | Quality trade-offs are explicit |
| Delivery | Frequent potentially shippable increments | Contract tests and idempotent event consumers | Controlled builds, approvals, and traceability | Protected behavior is verified |
| Planning | Rolling value-based selection | Modeling spikes and visible modeling debt | Range estimates, critical dependencies, contingency | Capacity and risk are visible |
| Architecture documentation | Context, key interface, and decision record | Selected stakeholder views, behavior, mappings, and rationale | Complete view package, traceability, active review, and debt record | Every documented contract is externally usable and current |
| Pattern selection | Choose the simplest pattern that solves the next slice | Prefer explicit domain, boundary, and integration patterns where complexity warrants them | Record alternatives, quality trade-offs, and evaluation evidence | A pattern is never selected only because it is fashionable |

Never remove: decision ownership, version identity, verification of protected behavior, change communication, and a path from production evidence back to planning.
