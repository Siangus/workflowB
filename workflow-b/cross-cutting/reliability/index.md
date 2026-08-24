# Reliability

Enable this module only when the project profile or current risk triggers it.

| State | Question |
|---|---|
| `problem-framing` | What assets, failure costs, obligations, or targets matter? |
| `requirements` | What must the system guarantee and how will it be measured? |
| `architecture` | Which boundaries, tactics, contracts, or patterns provide it? |
| `construction` | Which implementation controls must exist? |
| `verification` | What test or review evidence proves it? |
| `release` | What must be checked before exposure? |
| `operations` | What must be observed, controlled, and recovered? |

## Methods
- `KU-0045` [Availability and recovery tactics](../../L2/methods/KU-0045.md) - The system must continue or recover after component, network, dependency, or data-store failures.
- `KU-0073` [Production readiness and recovery mindset](../../L2/methods/KU-0073.md) - A feature is functionally complete but must face real users, traffic, dependencies, and failures.
- `KU-0075` [Stability patterns: timeouts, circuit breakers, bulkheads, and fail-fast](../../L2/methods/KU-0075.md) - A service calls remote, slow, unreliable, or resource-constrained dependencies.
- `KU-0076` [Steady state, back pressure, and load shedding](../../L2/methods/KU-0076.md) - Traffic can exceed processing capacity or downstream services can slow.
- `KU-0077` [Operational transparency and control](../../L2/methods/KU-0077.md) - A service runs across multiple instances, hosts, containers, or environments.
- `KU-0078` [Interconnect, load balancing, and service discovery](../../L2/methods/KU-0078.md) - A system has multiple instances, dynamic capacity, or service-to-service calls.
- `KU-0083` [Production-oriented testing and failure simulation](../../L2/methods/KU-0083.md) - A system has high availability, high traffic, or costly failure consequences.
- `KU-0085` [Chaos engineering as hypothesis-driven validation](../../L2/methods/KU-0085.md) - The system has established observability, safe abort controls, and a resilience hypothesis worth testing.
