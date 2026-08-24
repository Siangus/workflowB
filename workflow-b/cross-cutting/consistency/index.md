# Consistency and Idempotency

Enable this module only when the project profile or current risk triggers it.

| State | Question |
|---|---|
| `requirements` | What must the system guarantee and how will it be measured? |
| `architecture` | Which boundaries, tactics, contracts, or patterns provide it? |
| `construction` | Which implementation controls must exist? |
| `verification` | What test or review evidence proves it? |
| `release` | What must be checked before exposure? |

## Methods
- `KU-0019` [Aggregate consistency boundaries](../../L2/methods/KU-0019.md) - Defining domain objects that carry business rules or deciding transactional scope.
- `KU-0020` [Domain events and eventual consistency](../../L2/methods/KU-0020.md) - A state change must inform another aggregate or bounded context.
- `KU-0067` [Concurrency and transaction patterns](../../L2/methods/KU-0067.md) - Multiple requests can update the same business data or a business transaction spans separate system transactions.
- `KU-0075` [Stability patterns: timeouts, circuit breakers, bulkheads, and fail-fast](../../L2/methods/KU-0075.md) - A service calls remote, slow, unreliable, or resource-constrained dependencies.
- `KU-0076` [Steady state, back pressure, and load shedding](../../L2/methods/KU-0076.md) - Traffic can exceed processing capacity or downstream services can slow.
