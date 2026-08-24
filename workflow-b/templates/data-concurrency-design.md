# Data, Consistency, and Concurrency Design

Use this template only when durable data, concurrent updates, or distributed effects affect correctness.

## Authoritative Data and Constraints

| Fact / Entity | Owner / Authority | Identity | Fields and Meaning | Constraints / Indexes | Retention / Migration | Authoritative Query |
|---|---|---|---|---|---|---|

## Invariants and Transaction Boundaries

| Invariant / Rule ID | Business Transaction | System Transaction / Isolation | Conflict Detection / Locking | Success Fact | Failure Classification |
|---|---|---|---|---|---|

## Contention and Failure Traces

| Scenario ID | Actors / Requests | Interleaving or Fault | Expected Result per Actor | Durable Facts | Prohibited State | Recovery / Retry Semantics |
|---|---|---|---|---|---|---|

## Distributed Effect / Reconciliation

| Source Fact | Consumer / Replica | Delivery / Ordering / Idempotency | Partial Failure Behavior | Reconciliation / Compensation | Observation |
|---|---|---|---|---|---|
