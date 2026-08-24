# Observability and Control

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
- `KU-0054` [Architecture documentation, rationale, and debt](../../L2/methods/KU-0054.md) - A system has multiple stakeholders, non-obvious constraints, or architecture decisions likely to outlive the current team.
- `KU-0077` [Operational transparency and control](../../L2/methods/KU-0077.md) - A service runs across multiple instances, hosts, containers, or environments.
- `KU-0079` [Control plane and configuration management](../../L2/methods/KU-0079.md) - A system spans many instances, environments, versions, or operational services.
- `KU-0083` [Production-oriented testing and failure simulation](../../L2/methods/KU-0083.md) - A system has high availability, high traffic, or costly failure consequences.
