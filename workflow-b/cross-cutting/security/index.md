# Security

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
- `KU-0049` [Security as an architectural quality](../../L2/methods/KU-0049.md) - The system handles valuable data, privileged operations, external input, or untrusted components.
- `KU-0080` [Security as an ongoing production process](../../L2/methods/KU-0080.md) - The system handles user data, privileged operations, external input, or third-party dependencies.
