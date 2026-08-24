# Architecture and Domain Design Methods Index

Load only the method needed for the current activity.

| ID | Method | Trigger | Source |
|---|---|---|---|
| `KU-0015` | [Bounded contexts and ubiquitous language](../../L2/methods/KU-0015.md) | A complex domain contains terms with different meanings across business functions. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:226-563` |
| `KU-0017` | [Context mapping and integration relationships](../../L2/methods/KU-0017.md) | Two bounded contexts need to exchange behavior or information. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:748-1030` |
| `KU-0018` | [Anti-corruption layer and published integration language](../../L2/methods/KU-0018.md) | Integrating with legacy, external, or differently modeled systems. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:748-1030` |
| `KU-0019` | [Aggregate consistency boundaries](../../L2/methods/KU-0019.md) | Defining domain objects that carry business rules or deciding transactional scope. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:1031-1377` |
| `KU-0020` | [Domain events and eventual consistency](../../L2/methods/KU-0020.md) | A state change must inform another aggregate or bounded context. | `Domain-Driven_Design_Distilled_--_Vernon,_Vaughn_[Vernon,_Vaughn].md:1378-1713` |
| `KU-0043` | [Architecture as a quality-and-change decision structure](../../L2/methods/KU-0043.md) | A requirement, technology choice, or organizational constraint can affect multiple quality attributes or future change cost. | `extracted-book.md:603-803` |
| `KU-0044` | [Quality attribute scenarios](../../L2/methods/KU-0044.md) | A requirement says fast, secure, available, modifiable, testable, or deployable without measurable context. | `extracted-book.md:804-1056` |
| `KU-0045` | [Availability and recovery tactics](../../L2/methods/KU-0045.md) | The system must continue or recover after component, network, dependency, or data-store failures. | `extracted-book.md:1057-1291` |
| `KU-0047` | [Modifiability tactics](../../L2/methods/KU-0047.md) | The system must absorb new requirements, replace dependencies, or support multiple variants. | `extracted-book.md:1909-2101` |
| `KU-0048` | [Performance tactics and resource management](../../L2/methods/KU-0048.md) | The system has throughput, latency, capacity, or resource-use requirements. | `extracted-book.md:2288-2517` |
| `KU-0049` | [Security as an architectural quality](../../L2/methods/KU-0049.md) | The system handles valuable data, privileged operations, external input, or untrusted components. | `extracted-book.md:2886-3067` |
| `KU-0050` | [Testability as an architectural property](../../L2/methods/KU-0050.md) | Testing is expensive, slow, flaky, or cannot isolate architectural behavior. | `extracted-book.md:3068-3253` |
| `KU-0051` | [Architecturally significant requirements](../../L2/methods/KU-0051.md) | A requirement affects performance, availability, security, safety, deployability, modifiability, or system boundaries. | `extracted-book.md:4611-4791` |
| `KU-0052` | [Attribute-Driven Design](../../L2/methods/KU-0052.md) | The system has multiple quality drivers or a nontrivial architecture decision must be made before implementation. | `extracted-book.md:4990-5186` |
| `KU-0053` | [Architecture evaluation and ATAM](../../L2/methods/KU-0053.md) | Competing architectures or high-impact quality trade-offs require a decision. | `extracted-book.md:5187-5428` |
| `KU-0054` | [Architecture documentation, rationale, and debt](../../L2/methods/KU-0054.md) | A system has multiple stakeholders, non-obvious constraints, or architecture decisions likely to outlive the current team. | `extracted-book.md:5429-5676` |
| `KU-0055` | [Architecture viewtypes and styles](../../L2/methods/KU-0055.md) | A stakeholder needs to understand a structural, runtime, deployment, implementation, or work-assignment concern. | `Documenting software architectures 1-200.md:1625-1814` |
| `KU-0056` | [Module, component-connector, and allocation styles](../../L2/methods/KU-0056.md) | The architecture requires a shared vocabulary for structure, behavior, runtime interaction, or environment mapping. | `Documenting software architectures 1-200.md:2710-2908` |
| `KU-0057` | [Documenting architectural behavior](../../L2/methods/KU-0057.md) | Correctness, concurrency, real-time behavior, failure handling, or protocol use matters. | `Documenting software architectures 201-347.md:188-540` |
| `KU-0058` | [Usage-based view selection](../../L2/methods/KU-0058.md) | Starting or revising an architecture documentation package. | `Documenting software architectures 201-347.md:737-924` |
| `KU-0059` | [Architecture documentation package](../../L2/methods/KU-0059.md) | An architecture must be built, reviewed, transferred, or maintained by people who were not present for its creation. | `Documenting software architectures 201-347.md:1124-1463` |
| `KU-0060` | [Interface documentation](../../L2/methods/KU-0060.md) | A component, service, database, message, or external system is consumed by another party. | `Documenting software architectures 201-347.md:1464-1667` |
| `KU-0062` | [Variability and dynamism documentation](../../L2/methods/KU-0062.md) | A system supports plugins, configuration variants, dynamic binding, failover, hot deployment, or runtime reconfiguration. | `Documenting software architectures 201-347.md:1-187` |
| `KU-0063` | [Layering and responsibility boundaries](../../L2/methods/KU-0063.md) | An application has multiple kinds of change, complex domain logic, or several clients of the same business behavior. | `extracted-book.md:1-181` |
| `KU-0064` | [Choosing an organization for domain logic](../../L2/methods/KU-0064.md) | A team is deciding where business rules and use-case orchestration belong. | `extracted-book.md:1-181` |
| `KU-0065` | [Relational data-source patterns](../../L2/methods/KU-0065.md) | Domain objects must be persisted to a relational database or an existing schema. | `extracted-book.md:478-676` |
| `KU-0068` | [Session state and distribution boundaries](../../L2/methods/KU-0068.md) | A web or service application needs user/session state or is considering remote calls. | `extracted-book.md:1535-1760` |
| `KU-0071` | [Remote Facade and Data Transfer Object](../../L2/methods/KU-0071.md) | A service must be consumed across a process or network boundary. | `extracted-book.md:10947-11358` |
| `KU-0075` | [Stability patterns: timeouts, circuit breakers, bulkheads, and fail-fast](../../L2/methods/KU-0075.md) | A service calls remote, slow, unreliable, or resource-constrained dependencies. | `extracted-book.md:255-490` |
| `KU-0078` | [Interconnect, load balancing, and service discovery](../../L2/methods/KU-0078.md) | A system has multiple instances, dynamic capacity, or service-to-service calls. | `extracted-book.md:491-689` |
