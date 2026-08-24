# Performance and Capacity

Enable this module only when the project profile or current risk triggers it.

| State | Question |
|---|---|
| `requirements` | What must the system guarantee and how will it be measured? |
| `architecture` | Which boundaries, tactics, contracts, or patterns provide it? |
| `construction` | Which implementation controls must exist? |
| `verification` | What test or review evidence proves it? |
| `release` | What must be checked before exposure? |
| `operations` | What must be observed, controlled, and recovered? |

## Methods
- `KU-0048` [Performance tactics and resource management](../../L2/methods/KU-0048.md) - The system has throughput, latency, capacity, or resource-use requirements.
- `KU-0076` [Steady state, back pressure, and load shedding](../../L2/methods/KU-0076.md) - Traffic can exceed processing capacity or downstream services can slow.
- `KU-0078` [Interconnect, load balancing, and service discovery](../../L2/methods/KU-0078.md) - A system has multiple instances, dynamic capacity, or service-to-service calls.
- `KU-0083` [Production-oriented testing and failure simulation](../../L2/methods/KU-0083.md) - A system has high availability, high traffic, or costly failure consequences.
