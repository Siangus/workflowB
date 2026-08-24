# Design Readiness Methods Index

Load only the method needed for the current activity.

| ID | Method | Trigger | Source |
|---|---|---|---|
| `KU-0019` | [Aggregate consistency boundaries](../../L2/methods/KU-0019.md) | Defining domain objects that carry business rules or deciding transactional scope. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:1031-1377` |
| `KU-0020` | [Domain events and eventual consistency](../../L2/methods/KU-0020.md) | A state change must inform another aggregate or bounded context. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:1378-1713` |
| `KU-0031` | [Business-rule catalog and traceability](../../L2/methods/KU-0031.md) | Rules affect multiple requirements, products, or regulatory obligations. | `MinerU_markdown_软件需求（第3版）_(Karl_Wiegers,_Joy_Beatty)_(z-library.sk,_1lib.sk,_z-lib.sk)_1-200.md:3478-3821` |
| `KU-0033` | [Requirements modeling](../../L2/methods/KU-0033.md) | Text requirements contain complex workflows, decisions, data relationships, or stateful behavior. | `MinerU_markdown_软件需求（第3版）_(Karl_Wiegers,_Joy_Beatty)_(z-library.sk,_1lib.sk,_z-lib.sk)_1-200.md:532-732` |
| `KU-0034` | [Quantified quality attributes and constraints](../../L2/methods/KU-0034.md) | A system has performance, reliability, security, usability, interoperability, scalability, or other quality concerns. | `MinerU_markdown_软件需求（第3版）_(Karl_Wiegers,_Joy_Beatty)_(z-library.sk,_1lib.sk,_z-lib.sk)_1-200.md:914-1252` |
| `KU-0037` | [Requirements validation through review and acceptance criteria](../../L2/methods/KU-0037.md) | A requirement set is ready for baseline, iteration commitment, or implementation. | `MinerU_markdown_软件需求（第3版）_(Karl_Wiegers,_Joy_Beatty)_(z-library.sk,_1lib.sk,_z-lib.sk)_1-200.md:2774-3130` |
| `KU-0044` | [Quality attribute scenarios](../../L2/methods/KU-0044.md) | A requirement says fast, secure, available, modifiable, testable, or deployable without measurable context. | `extracted-book.md:804-1056` |
| `KU-0052` | [Attribute-Driven Design](../../L2/methods/KU-0052.md) | The system has multiple quality drivers or a nontrivial architecture decision must be made before implementation. | `extracted-book.md:4990-5186` |
| `KU-0053` | [Architecture evaluation and ATAM](../../L2/methods/KU-0053.md) | Competing architectures or high-impact quality trade-offs require a decision. | `extracted-book.md:5187-5428` |
| `KU-0059` | [Architecture documentation package](../../L2/methods/KU-0059.md) | An architecture must be built, reviewed, transferred, or maintained by people who were not present for its creation. | `Documenting software architectures 201-347.md:1124-1463` |
| `KU-0060` | [Interface documentation](../../L2/methods/KU-0060.md) | A component, service, database, message, or external system is consumed by another party. | `Documenting software architectures 201-347.md:1464-1667` |
| `KU-0067` | [Concurrency and transaction patterns](../../L2/methods/KU-0067.md) | Multiple requests can update the same business data or a business transaction spans separate system transactions. | `extracted-book.md:1110-1534` |
| `KU-0075` | [Stability patterns: timeouts, circuit breakers, bulkheads, and fail-fast](../../L2/methods/KU-0075.md) | A service calls remote, slow, unreliable, or resource-constrained dependencies. | `extracted-book.md:255-490` |
| `KU-0081` | [Deployment automation and continuous delivery](../../L2/methods/KU-0081.md) | A team must release changes regularly or recover from a failed deployment. | `extracted-book.md:690-819` |
| `KU-0083` | [Production-oriented testing and failure simulation](../../L2/methods/KU-0083.md) | A system has high availability, high traffic, or costly failure consequences. | `extracted-book.md:690-819` |
