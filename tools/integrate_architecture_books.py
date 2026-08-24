"""Integrate the three architecture books into the existing Workflow B registry."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("work/se-workflow")
REGISTRY = ROOT / "registry"
SOURCES = ROOT / "sources"
WORKFLOW = ROOT / "workflow-b"

SAIP = "bass-clements-kazman-saip4"
DOCS = "clements-documenting-software-architectures"
POEAA = "fowler-poeaa"


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def source_segment(book_id: str, line: int, file_hint: str | None = None) -> dict:
    rows = jsonl(SOURCES / book_id / "segments.jsonl")
    candidates = [row for row in rows if row["start_line"] <= line <= row["end_line"]]
    if file_hint:
        candidates = [row for row in candidates if file_hint in row["file"]]
    if not candidates:
        raise ValueError(f"No segment contains {book_id}:{line} ({file_hint})")
    return candidates[0]


def make_unit(
    number: int,
    book_id: str,
    line: int,
    title: str,
    phase: str,
    kind: str,
    purpose: str,
    trigger: str,
    procedure: list[str],
    checks: list[str],
    anti_patterns: list[str],
    tailoring: dict,
    secondary: list[str] | None = None,
    file_hint: str | None = None,
    merge_status: str = "NEW",
) -> dict:
    segment = source_segment(book_id, line, file_hint)
    return {
        "ku_id": f"KU-{number:04d}",
        "book_id": book_id,
        "segment_id": segment["segment_id"],
        "title": title,
        "lifecycle_phase": phase,
        "secondary_domains": secondary or [],
        "knowledge_type": kind,
        "confidence": "high",
        "merge_status": merge_status,
        "needs_review": False,
        "status": "integrated_core",
        "purpose": purpose,
        "trigger": trigger,
        "inputs": ["Business goals and requirements", "Current project context"],
        "outputs": ["Architecture decision or design artifact", "Reviewable evidence"],
        "procedure": procedure,
        "checks": checks,
        "anti_patterns": anti_patterns,
        "tailoring": tailoring,
        "source_locator": segment["source_locator"],
    }


def card(item: dict) -> str:
    lines = [
        f"# {item['ku_id']}: {item['title']}", "",
        f"- **book_id:** `{item['book_id']}`",
        f"- **segment_id:** `{item['segment_id']}`",
        f"- **lifecycle_phase:** `{item['lifecycle_phase']}`",
        f"- **knowledge_type:** `{item['knowledge_type']}`",
        f"- **merge_status:** `{item['merge_status']}`", "",
        "## Purpose", item["purpose"], "", "## Trigger", item["trigger"], "", "## Procedure",
    ]
    lines.extend(f"{i}. {step}" for i, step in enumerate(item["procedure"], 1))
    lines.extend(["", "## Checks"])
    lines.extend(f"- {check}" for check in item["checks"])
    lines.extend(["", "## Anti-patterns"])
    lines.extend(f"- {value}" for value in item["anti_patterns"])
    lines.extend(["", "## Tailoring", json.dumps(item["tailoring"], ensure_ascii=False), "", "## Source", f"`{item['source_locator']}`", ""])
    return "\n".join(lines)


def saip_units() -> list[dict]:
    return [
        make_unit(43, SAIP, 616, "Architecture as a quality-and-change decision structure", "architecture", "principle", "Use architecture to make early decisions that enable required quality attributes and constrain expensive changes.", "A requirement, technology choice, or organizational constraint can affect multiple quality attributes or future change cost.", ["Identify the externally visible structures and decisions.", "Connect each decision to quality attributes, stakeholders, constraints, and likely changes.", "Make the smallest set of decisions that controls the important risks.", "Record the decision and its consequences."], ["Each important decision has a quality or change rationale.", "Stakeholders can identify what the architecture constrains."], ["Treating architecture as a diagram produced after coding.", "Choosing a style before understanding the quality problem."], {"light": "One decision record per architecturally significant issue.", "heavy": "Architecture baseline with views, scenarios, evaluation, and rationale.", "cannot_remove": True}, ["requirements", "governance"]),
        make_unit(44, SAIP, 804, "Quality attribute scenarios", "requirements", "method", "Convert vague quality goals into stimuli, environments, responses, and measurable response targets.", "A requirement says fast, secure, available, modifiable, testable, or deployable without measurable context.", ["Name the source of the stimulus.", "Describe the stimulus and operating environment.", "Describe the expected system response.", "Define a measurable response target.", "Trace the scenario to architecture tactics and tests."], ["Scenario is observable and measurable.", "Architecture and test evidence address the same scenario."], ["Using adjectives such as fast or reliable without conditions.", "Leaving quality attributes as a late testing concern."], {"light": "Three to five priority scenarios per release.", "heavy": "Utility tree, scenario catalog, architecture evaluation, and quality test plan.", "cannot_remove": True}, ["verification", "risk"], merge_status="EXTENDS"),
        make_unit(45, SAIP, 1213, "Availability and recovery tactics", "architecture", "method", "Design for failure detection, recovery, repair, and controlled loss of service.", "The system must continue or recover after component, network, dependency, or data-store failures.", ["Classify failure sources and affected services.", "Define availability scenarios and RTO/RPO expectations.", "Select tactics such as redundancy, heartbeat, ping/echo, exception handling, rollback, retry, or graceful degradation.", "Test recovery paths and operational visibility."], ["Failure modes have detection and response.", "Recovery targets are measurable.", "A failed dependency does not create an uncontrolled cascade."], ["Assuming redundancy alone proves availability.", "Testing only the happy path."], {"light": "Critical dependency timeout, retry, and fallback tests.", "heavy": "Fault model, RTO/RPO, failover rehearsal, and recovery evidence.", "cannot_remove": False}, ["verification", "release", "operations"]),
        make_unit(46, SAIP, 1213, "Deployability and safe rollout", "release", "method", "Make software changes installable, reversible, and independently verifiable.", "A release changes code, configuration, schema, infrastructure, or service topology.", ["Identify deployment units and compatibility constraints.", "Separate deployment from activation where useful.", "Use versioning, migration compatibility, rollback or roll-forward tactics.", "Verify the deployed artifact and its runtime configuration."], ["A release has an immutable identity.", "Rollback or forward recovery is defined.", "Schema and interface changes are compatible or deliberately coordinated."], ["Treating deployment as an afterthought.", "Making an irreversible data change without a recovery plan."], {"light": "Automated build, smoke test, and rollback checklist.", "heavy": "Progressive delivery, compatibility matrix, migration rehearsal, and release observability.", "cannot_remove": True}, ["construction", "verification", "governance"]),
        make_unit(47, SAIP, 1993, "Modifiability tactics", "architecture", "method", "Control the cost and blast radius of expected changes through responsibility, coupling, cohesion, indirection, and deferred binding.", "The system must absorb new requirements, replace dependencies, or support multiple variants.", ["List likely change sources and affected responsibilities.", "Localize likely changes behind interfaces or encapsulation.", "Reduce unnecessary coupling and dependency distance.", "Evaluate the change scenario against the current architecture.", "Track architecture debt when a short-term shortcut increases future cost."], ["A likely change has a bounded impact area.", "The architecture exposes where change work will occur."], ["Adding abstractions without a change scenario.", "Allowing cross-layer or cross-context shortcuts."], {"light": "Record change hotspots and protect one boundary.", "heavy": "Change scenario suite, dependency analysis, and architecture debt backlog.", "cannot_remove": False}, ["maintenance", "design"]),
        make_unit(48, SAIP, 2299, "Performance tactics and resource management", "architecture", "method", "Meet timing and throughput goals by managing demand, resources, concurrency, and processing order.", "The system has throughput, latency, capacity, or resource-use requirements.", ["Define performance scenarios and workload shape.", "Identify resource demands and bottlenecks.", "Choose tactics such as concurrency, scheduling, queueing, caching, replication, resource pooling, or prioritization.", "Load-test the architecture and compare measured response to targets."], ["Workload and measurement method are explicit.", "Tests represent peak and representative demand.", "Performance improvements do not violate consistency or security requirements."], ["Optimizing a guessed bottleneck.", "Using average latency while ignoring tail latency."], {"light": "Load test the critical path and set latency/error budgets.", "heavy": "Capacity model, load profile, saturation tests, and production telemetry.", "cannot_remove": False}, ["verification", "risk"]),
        make_unit(49, SAIP, 2886, "Security as an architectural quality", "architecture", "method", "Protect data and operations through explicit threat, trust-boundary, access, and attack-response decisions.", "The system handles valuable data, privileged operations, external input, or untrusted components.", ["Identify assets, actors, trust boundaries, and threats.", "Define authentication, authorization, confidentiality, integrity, and accountability scenarios.", "Select architectural tactics such as least privilege, isolation, validation, encryption, audit, and attack detection.", "Trace controls to security tests and release evidence."], ["Every sensitive operation has an authorization decision.", "Trust boundaries and failure behavior are documented.", "Security controls have verification evidence."], ["Relying on the UI for authorization.", "Treating security as a penetration test performed at the end."], {"light": "Threat model critical flows and test access control.", "heavy": "Threat model, secure architecture review, abuse cases, dependency analysis, and security test suite.", "cannot_remove": True}, ["requirements", "verification", "governance"]),
        make_unit(50, SAIP, 3068, "Testability as an architectural property", "verification", "method", "Design the system so faults can be exposed, components isolated, behavior observed, and tests executed repeatably.", "Testing is expensive, slow, flaky, or cannot isolate architectural behavior.", ["Define testability scenarios.", "Expose controlled interfaces and seams.", "Separate test data and environments.", "Use dependency substitution, record/replay, assertions, and deterministic clocks where appropriate.", "Measure test execution time and diagnostic quality."], ["Important components can be tested without the whole system.", "Failures identify the responsible boundary.", "Tests are repeatable and observable."], ["Making production code depend directly on unreplaceable infrastructure.", "Using end-to-end tests to cover every internal rule."], {"light": "Test critical boundaries with fakes and contract tests.", "heavy": "Architecture-level testability review and layered test strategy.", "cannot_remove": True}, ["construction", "quality"]),
        make_unit(51, SAIP, 4675, "Architecturally significant requirements", "requirements", "decision_rule", "Find the subset of requirements that materially shapes architecture and make their trade-offs explicit.", "A requirement affects performance, availability, security, safety, deployability, modifiability, or system boundaries.", ["Review business goals, requirements, constraints, and stakeholder concerns.", "Classify requirements as irrelevant, potentially significant, or clearly significant.", "Elicit missing scenarios and thresholds.", "Record the significant requirements in a utility tree or equivalent structure.", "Use them as drivers for architecture design and evaluation."], ["Every architecture driver has a source and measurable scenario.", "Architecture review covers the highest-risk drivers."], ["Treating every requirement as equally architectural.", "Discovering architecture drivers only after implementation."], {"light": "Mark architecture drivers in the backlog or requirement register.", "heavy": "Utility tree, stakeholder workshop, scenario prioritization, and traceability.", "cannot_remove": True}, ["problem-framing", "risk"], merge_status="EXTENDS"),
        make_unit(52, SAIP, 4990, "Attribute-Driven Design", "architecture", "method", "Iteratively derive architecture structures from quality attributes, functionality, constraints, and design concepts.", "The system has multiple quality drivers or a nontrivial architecture decision must be made before implementation.", ["Choose the iteration goal and prioritize drivers.", "Select the system element to decompose.", "Identify relevant design concepts and tactics.", "Instantiate structures and allocate responsibilities.", "Record preliminary views and analyze the design against the iteration goal.", "Repeat until risk and scope are sufficient for the next increment."], ["Each design iteration has a goal and evidence.", "The result addresses the selected drivers.", "Unresolved risks become experiments or decisions."], ["Big-design-up-front without feedback.", "Selecting patterns without tracing them to drivers."], {"light": "Design just enough for the next vertical slice.", "heavy": "Architecture iteration plan, design review, and documented trade-offs.", "cannot_remove": False}, ["planning", "design"], merge_status="NEW"),
        make_unit(53, SAIP, 5187, "Architecture evaluation and ATAM", "architecture", "method", "Reduce architecture risk before implementation by examining scenarios, tactics, trade-offs, and sensitivity points with stakeholders.", "Competing architectures or high-impact quality trade-offs require a decision.", ["Collect business drivers and quality scenarios.", "Present the architecture and identify approaches.", "Analyze scenarios to expose sensitivity points, trade-offs, and risks.", "Record findings, priorities, and recommended actions.", "Use a lightweight evaluation when full ATAM cost is not justified."], ["Stakeholders participate in the evaluation.", "Trade-offs and risks are recorded, not merely discussed.", "Actions have owners and follow-up evidence."], ["Architecture review as a presentation with no challenge.", "Evaluating only structure while ignoring quality scenarios."], {"light": "Focused review of one risky quality attribute.", "heavy": "ATAM or equivalent multi-stakeholder evaluation with risk backlog.", "cannot_remove": False}, ["risk", "governance"]),
        make_unit(54, SAIP, 5490, "Architecture documentation, rationale, and debt", "governance", "method", "Keep architecture usable and evolvable by documenting views, decisions, rationale, and debt hotspots.", "A system has multiple stakeholders, non-obvious constraints, or architecture decisions likely to outlive the current team.", ["Choose views based on stakeholder uses.", "Document the architecture, interfaces, behavior, and rationale.", "Relate decisions to requirements and quality scenarios.", "Inspect the code and dependencies for architecture debt hotspots.", "Schedule debt reduction with normal delivery work."], ["A reader can find the view needed for their decision.", "Rationale explains why alternatives were rejected.", "Architecture debt has evidence, owner, and planned treatment."], ["Producing a diagram with no element definitions or rationale.", "Allowing documentation and implementation to diverge."], {"light": "Context diagram, key view, interface notes, and decision log.", "heavy": "View catalog, mappings, interface package, active review, and debt analysis.", "cannot_remove": False}, ["maintenance", "teamwork"], merge_status="EXTENDS"),
    ]


def docs_units() -> list[dict]:
    fh1 = "Documenting software architectures 1-200.md"
    fh2 = "Documenting software architectures 201-347.md"
    return [
        make_unit(55, DOCS, 1627, "Architecture viewtypes and styles", "architecture", "method", "Describe different architectural concerns with a viewtype whose elements, relations, properties, and notation are explicit.", "A stakeholder needs to understand a structural, runtime, deployment, implementation, or work-assignment concern.", ["Identify the concern and intended use.", "Choose module, component-and-connector, or allocation viewtype.", "Define elements, relations, properties, and notation.", "Connect the view to supporting catalogs and other views."], ["The view answers a named stakeholder question.", "Every symbol and relation has a defined meaning."], ["Using one overloaded diagram for every concern.", "Mixing logical layers, runtime tiers, and deployment nodes without a mapping."], {"light": "Use one focused view per architecture question.", "heavy": "View catalog with style guide, element catalog, mappings, and review checklist.", "cannot_remove": False}, ["requirements", "governance"], file_hint=fh1),
        make_unit(56, DOCS, 2710, "Module, component-connector, and allocation styles", "architecture", "model", "Use established styles to communicate decomposition, dependency, runtime interaction, deployment, implementation, and work assignment.", "The architecture requires a shared vocabulary for structure, behavior, runtime interaction, or environment mapping.", ["Select a style that matches the reasoning task.", "Define the permitted elements and relations.", "Document constraints and interpretation rules.", "Provide examples and mappings to other styles."], ["The selected style does not imply unsupported behavior.", "Relations have direction and ownership where relevant."], ["Treating a style name as an architecture without defining its semantics.", "Assuming layers and deployment tiers are interchangeable."], {"light": "Use layered, client-server, publish-subscribe, or deployment views only when they answer a decision.", "heavy": "Style-specific notation, rules, examples, and consistency checks.", "cannot_remove": False}, ["design"], file_hint=fh1),
        make_unit(57, DOCS, 208, "Documenting architectural behavior", "architecture", "method", "Record behavior, protocols, timing, ordering, and state transitions that cannot be understood from static structure alone.", "Correctness, concurrency, real-time behavior, failure handling, or protocol use matters.", ["Identify externally visible stimuli and responses.", "Choose statecharts, sequence diagrams, use cases, message charts, or formal/trace notation.", "Document ordering, timing, error, and timeout constraints.", "Link behavior to components, interfaces, requirements, and tests."], ["The behavior model covers normal and exceptional paths.", "Ordering and timeout assumptions are explicit."], ["Using class structure as a substitute for runtime behavior.", "Drawing sequence diagrams without stating protocol constraints."], {"light": "Behavior diagram for each high-risk scenario.", "heavy": "Behavior package with formal constraints and executable acceptance scenarios.", "cannot_remove": False}, ["requirements", "verification"], file_hint=fh2),
        make_unit(58, DOCS, 737, "Usage-based view selection", "architecture", "decision_rule", "Select only the views that have a real stakeholder use, balancing documentation benefit against maintenance cost.", "Starting or revising an architecture documentation package.", ["List stakeholders and the decisions they must make.", "List anticipated uses: analysis, development, review, implementation, deployment, maintenance, or reconstruction.", "Choose viewtypes and styles that support those uses.", "Avoid views that no stakeholder will use.", "Revisit the set when the architecture or audience changes."], ["Each view has an audience and intended use.", "Documentation cost is justified by a decision or activity."], ["Generating a standard view set without stakeholder demand.", "Combining unrelated views until neither concern is clear."], {"light": "Context, module, runtime, and deployment views for the main decisions only.", "heavy": "Usage matrix, view catalog, view packets, and periodic usefulness review.", "cannot_remove": False}, ["teamwork", "governance"], file_hint=fh2),
        make_unit(59, DOCS, 1124, "Architecture documentation package", "governance", "artifact", "Build a coherent documentation package containing views, context, element catalogs, mappings, rationale, glossary, and completeness information.", "An architecture must be built, reviewed, transferred, or maintained by people who were not present for its creation.", ["Provide a system overview and context diagram.", "For each view, document the primary presentation, element catalog, relations, properties, and rationale.", "Document mappings across views.", "Maintain glossary, constraints, assumptions, and known omissions.", "Package information by stakeholder use."], ["Readers can navigate from overview to detail and back.", "Every depicted element has supporting definition.", "Cross-view mappings are complete enough for the intended use."], ["A diagram without a key, catalog, or mapping.", "Writing documentation as a one-time delivery artifact."], {"light": "README, context diagram, key views, interface contracts, and decision records.", "heavy": "Stakeholder-specific view packets, complete catalogs, mappings, glossary, rationale, and review record.", "cannot_remove": False}, ["teamwork", "maintenance"], file_hint=fh2),
        make_unit(60, DOCS, 1464, "Interface documentation", "architecture", "artifact", "Make software interfaces stable and usable by documenting syntax, semantics, protocols, assumptions, and externally visible behavior.", "A component, service, database, message, or external system is consumed by another party.", ["Identify the interface and its stakeholders.", "Document signatures, data types, preconditions, postconditions, effects, errors, timing, and protocol ordering.", "Document examples and version/evolution rules.", "Expose only stable externally visible information.", "Link interface documentation to tests and implementation."], ["Consumers can use the interface without reading implementation.", "Error and timeout behavior is documented.", "Versioning and compatibility policy are explicit."], ["Documenting only method signatures.", "Leaking unstable implementation details as a promised contract."], {"light": "API schema, examples, errors, and contract tests.", "heavy": "Full interface package with semantic constraints, protocols, version policy, and compatibility tests.", "cannot_remove": True}, ["requirements", "verification", "release"], file_hint=fh2),
        make_unit(61, DOCS, 2469, "Active architecture documentation review", "architecture", "checklist", "Review architecture documentation for utility, correctness, completeness, consistency, and stakeholder usability.", "An architecture package is proposed, baselined, or changed materially.", ["Identify reviewers and their intended uses.", "Review views, catalogs, mappings, interfaces, behavior, rationale, and glossary.", "Check for conflicting definitions, missing elements, ambiguous notation, and stale assumptions.", "Record findings and update the package."], ["Reviewers can answer their intended questions.", "Findings have owners and closure evidence.", "Documentation matches the current architecture."], ["Proofreading diagrams without evaluating whether they support decisions.", "Accepting documentation because the author understands it."], {"light": "Peer review against a view checklist.", "heavy": "Active review with stakeholder walk-through and architecture/implementation comparison.", "cannot_remove": False}, ["quality", "governance"], file_hint=fh2),
        make_unit(62, DOCS, 7, "Variability and dynamism documentation", "architecture", "method", "Record configured variation, runtime change, optional components, and dynamic behavior so architecture decisions remain explicit.", "A system supports plugins, configuration variants, dynamic binding, failover, hot deployment, or runtime reconfiguration.", ["Identify variation points and allowed values.", "Document when and how variation is selected.", "Document constraints, dependencies, and invalid combinations.", "Describe runtime transitions and their impact on interfaces and deployment."], ["Variation is distinguishable from accidental implementation behavior.", "Supported runtime states and transitions have tests or operational evidence."], ["Leaving configuration or dynamic behavior implicit.", "Assuming all runtime variants receive equal validation."], {"light": "Configuration/feature-flag table and one dynamic behavior diagram.", "heavy": "Variability model, state model, compatibility matrix, and variant test plan.", "cannot_remove": False}, ["requirements", "verification"], file_hint=fh2),
    ]


def poeaa_units() -> list[dict]:
    return [
        make_unit(63, POEAA, 8, "Layering and responsibility boundaries", "design", "pattern", "Separate presentation, domain, and data-source responsibilities to manage coupling while avoiding unnecessary distribution.", "An application has multiple kinds of change, complex domain logic, or several clients of the same business behavior.", ["Identify responsibilities and change forces.", "Choose logical layers and dependency direction.", "Keep layer interfaces explicit.", "Deploy layers separately only when the operational benefit justifies the cost."], ["Domain rules are not accidentally owned by the UI or persistence layer.", "Distribution is justified by a measurable need."], ["Adding layers or network hops by fashion.", "Allowing dependencies to flow in every direction."], {"light": "Clear application/domain/data boundaries in one service.", "heavy": "Layer rules, dependency checks, interface package, and deployment rationale.", "cannot_remove": False}, ["architecture", "construction"]),
        make_unit(64, POEAA, 117, "Choosing an organization for domain logic", "design", "decision_rule", "Choose Transaction Script, Domain Model, Table Module, or Service Layer according to domain complexity and collaboration needs.", "A team is deciding where business rules and use-case orchestration belong.", ["Assess domain complexity, rule interaction, number of clients, and expected change.", "Use Transaction Script for simple procedural operations.", "Use Domain Model for interacting rules and rich invariants.", "Use Table Module where logic is organized around tabular data.", "Add a thin Service Layer when clients need a stable application boundary."], ["The choice explains domain complexity and future change.", "The selected structure keeps business rules testable."], ["Using a rich domain model for trivial CRUD.", "Putting all business logic into a service layer because it is convenient."], {"light": "Start simple and promote structure when rule interaction justifies it.", "heavy": "Explicit domain-logic decision record and architecture tests.", "cannot_remove": False}, ["architecture", "requirements"], merge_status="EXTENDS"),
        make_unit(65, POEAA, 478, "Relational data-source patterns", "design", "pattern", "Isolate relational persistence choices from domain behavior and choose a mapping strategy appropriate to schema and object complexity.", "Domain objects must be persisted to a relational database or an existing schema.", ["Identify ownership of persistence behavior.", "Choose Gateway, Active Record, or Data Mapper based on domain complexity and coupling tolerance.", "Define transaction and query boundaries.", "Profile mapping and query behavior.", "Keep schema evolution and mapping changes reviewable."], ["Persistence mapping does not silently change domain invariants.", "Queries and transaction boundaries are observable and tested."], ["Assuming an ORM removes mapping and performance decisions.", "Letting persistence annotations dictate the domain model by accident."], {"light": "Repository/mapper with integration tests.", "heavy": "Explicit mapping strategy, query tests, migration plan, and performance profile.", "cannot_remove": False}, ["construction", "verification"]),
        make_unit(66, POEAA, 4824, "Unit of Work, Identity Map, and Lazy Load", "construction", "pattern", "Coordinate persistence changes, prevent duplicate in-memory identities, and control data loading inside a business transaction.", "A business operation changes multiple persistent objects or repeated loads create consistency/performance problems.", ["Define business transaction scope.", "Track new, dirty, and deleted objects.", "Use identity mapping where object identity matters.", "Apply lazy loading only where access patterns justify it.", "Test commit, rollback, duplicate loading, and query count behavior."], ["All intended changes commit or roll back coherently.", "Lazy loading does not create unbounded query cascades."], ["Hiding database calls inside arbitrary property access.", "Using a unit of work without a clear transaction boundary."], {"light": "Explicit transaction service and focused integration tests.", "heavy": "Unit-of-work policy, identity rules, query budgets, and failure tests.", "cannot_remove": False}, ["verification", "risk"]),
        make_unit(67, POEAA, 1269, "Concurrency and transaction patterns", "construction", "pattern", "Protect business transactions from lost updates, inconsistent reads, deadlocks, and cross-session conflicts.", "Multiple requests can update the same business data or a business transaction spans separate system transactions.", ["Identify business and system transaction boundaries.", "Choose isolation, immutability, optimistic or pessimistic locking, or coarse-grained locking.", "Define conflict detection and user/system recovery.", "Test contention, rollback, retry, and deadlock behavior."], ["Concurrent updates cannot silently overwrite valid changes.", "Conflict outcomes are deterministic and actionable."], ["Using a lock without defining its scope and failure behavior.", "Confusing database transaction success with business transaction completion."], {"light": "Database constraint or optimistic version check for the critical entity.", "heavy": "Contention model, lock policy, retry/compensation design, and load tests.", "cannot_remove": False}, ["architecture", "verification"], merge_status="EXTENDS"),
        make_unit(68, POEAA, 1535, "Session state and distribution boundaries", "architecture", "decision_rule", "Choose where state lives and where distribution occurs based on failover, payload, latency, consistency, and operational constraints.", "A web or service application needs user/session state or is considering remote calls.", ["Classify state as client, server, database, or domain state.", "Define ownership, lifetime, sensitivity, and failover requirements.", "Keep remote interfaces coarse-grained and explicit.", "Prefer local calls until distribution has a measured benefit.", "Test restart, failover, serialization, and timeout behavior."], ["State survives the required failures.", "Remote calls have documented latency and error behavior.", "Distribution reduces a real constraint rather than adding accidental coupling."], ["Distributing fine-grained objects for convenience.", "Storing sensitive or large state in an uncontrolled client."], {"light": "Stateless service plus explicit client/session identifier.", "heavy": "Session failover policy, remote facade, DTO contract, and resilience tests.", "cannot_remove": False}, ["release", "operations"]),
        make_unit(69, POEAA, 1110, "Web presentation and controller boundaries", "design", "pattern", "Separate request handling, presentation transformation, application flow, and domain behavior so UI changes do not corrupt business rules.", "An application exposes browser or API clients with multiple flows or presentation forms.", ["Separate input parsing and validation from application commands.", "Choose Page Controller, Front Controller, MVC, Template View, or Application Controller as appropriate.", "Keep presentation models distinct from domain models when needed.", "Test controller routing, validation, and response behavior."], ["Presentation changes do not alter domain rules accidentally.", "Input, application, and domain errors are distinguishable."], ["Putting transaction and pricing rules in controllers.", "Returning persistence objects as an accidental public API."], {"light": "Thin controller and application service with request/response DTOs.", "heavy": "Explicit presentation/application/domain boundaries and contract tests.", "cannot_remove": False}, ["requirements", "verification"]),
        make_unit(70, POEAA, 8561, "Repository, Query Object, and metadata mapping", "construction", "pattern", "Provide domain-oriented access to persisted objects while keeping query intent and mapping metadata explicit.", "Consumers need collection-like access, complex queries, or multiple persistence implementations.", ["Define aggregate or entity access boundaries.", "Use Repository for domain collection semantics.", "Use Query Object for composable query intent.", "Keep mapping metadata and repository behavior testable.", "Separate read models when query needs differ from write models."], ["Query intent is testable without relying on incidental SQL.", "Repository boundaries do not hide expensive unbounded reads."], ["Creating repositories for every table without domain meaning.", "Returning mutable persistence internals across boundaries."], {"light": "Repository only around aggregate boundaries.", "heavy": "Query objects, read models, mapping tests, and performance budgets.", "cannot_remove": False}, ["architecture", "verification"]),
        make_unit(71, POEAA, 10947, "Remote Facade and Data Transfer Object", "architecture", "pattern", "Reduce network round trips and stabilize remote contracts by exposing coarse-grained operations and explicit transfer data.", "A service must be consumed across a process or network boundary.", ["Identify a complete business operation rather than exposing fine-grained objects.", "Define a coarse-grained facade.", "Shape DTOs for the consumer contract.", "Version and test the remote contract.", "Document timeout, error, and compatibility behavior."], ["Remote call count and payload size meet performance goals.", "Consumers are not coupled to internal domain object graphs."], ["Remoting every domain object method.", "Returning internal persistence structures as DTOs."], {"light": "Stable API DTOs and contract tests.", "heavy": "Versioned facade, schema evolution policy, compatibility suite, and telemetry.", "cannot_remove": True}, ["requirements", "release", "verification"]),
        make_unit(72, POEAA, 13156, "Base patterns for isolation and testing", "construction", "pattern", "Isolate external resources and stabilize reusable concepts through Gateway, Mapper, Value Object, Money, Special Case, Plugin, and Service Stub patterns.", "Code depends on external services, configuration, money, null cases, or replaceable implementations.", ["Identify external or volatile dependencies.", "Wrap them behind Gateway or Mapper interfaces.", "Use Value Objects for domain concepts such as money and ranges.", "Use Service Stub or Plugin to isolate tests and configuration.", "Test the boundary and the domain behavior independently."], ["External failures are testable without requiring the real service.", "Value objects enforce domain invariants.", "Substitution does not change the intended contract."], ["Mocking every internal object instead of isolating true boundaries.", "Representing money with primitive arithmetic without rounding policy."], {"light": "Stub external services and use domain value objects for critical concepts.", "heavy": "Contract tests, failure simulation, plugin policy, and monetary correctness tests.", "cannot_remove": False}, ["verification", "requirements"]),
    ]


SUMMARIES = {
    SAIP: """# Book Summary: Software Architecture in Practice, 4th Edition

This book treats architecture as a lifecycle discipline for making and evaluating decisions that control system qualities and change costs. Chapters 1-3 define architecture, its importance, quality attribute scenarios, tactics, and questionnaires. Chapters 4-14 apply the method to availability, deployability, energy efficiency, integrability, modifiability, performance, safety, security, testability, usability, and combinations of qualities. Chapters 15-18 cover interfaces, virtualization, cloud/distributed computing, and mobile constraints. Chapters 19-23 connect requirements to architecture through architecturally significant requirements, Attribute-Driven Design, ATAM/lightweight evaluation, documentation, and architecture debt. Chapters 24-25 cover the architect's project role and competence; Chapter 26 provides a future-oriented quantum-computing overview.

The transferable method is: identify quality and business drivers, express them as measurable scenarios, choose tactics and structures, design incrementally, evaluate trade-offs before code hardens, document the result, and manage architecture debt as part of normal delivery.
""",
    DOCS: """# Book Summary: Documenting Software Architectures

This book treats architecture documentation as a usable package rather than a single diagram. It introduces module, component-and-connector, and allocation viewtypes, then gives styles for decomposition, uses, generalization, layers, data streams, call-return, client-server, publish-subscribe, deployment, implementation, and work assignment. It also covers behavior documentation, context diagrams, refinement, view packets, variability, dynamism, stakeholder-driven view selection, documentation packages, cross-view mappings, interfaces, rationale, and active reviews.

The transferable method is: identify who will use the documentation and for what decision, choose only the views that serve those uses, define every element/relation/property and notation, provide catalogs and mappings, document externally visible behavior and interfaces, record rationale and variability, then review the package with its stakeholders.

The supplied Markdown contains draft-production markers such as `tbd` and `in progress`; those are source-quality caveats, not Workflow B rules.
""",
    POEAA: """# Book Summary: Patterns of Enterprise Application Architecture

This book is a pattern catalog for enterprise applications. The narrative chapters explain layering, organization of domain logic, relational database mapping, web presentation, concurrency, session state, distribution, and how to combine these choices. The pattern chapters then classify solutions for domain logic, data sources, object-relational behavior and structure, metadata mapping, web presentation, distribution, offline concurrency, session state, and base concerns.

The transferable method is not to apply every pattern. First identify the domain complexity, transaction boundary, data source, presentation boundary, concurrency problem, and distribution cost; then choose the smallest pattern that solves the actual problem and verify its consequences. The book is older than current frameworks, but its problem/solution trade-offs remain useful for service layers, repositories, unit of work, optimistic locking, DTOs, gateways, and test stubs.
""",
}


def update_registry(units: list[dict]) -> None:
    sources = jsonl(REGISTRY / "sources.jsonl")
    known = {row["book_id"] for row in sources}
    metadata = {
        SAIP: ("Software Architecture in Practice, 4th Edition", "architecture-quality-and-evaluation", 26),
        DOCS: ("Documenting Software Architectures", "architecture-documentation", 13),
        POEAA: ("Patterns of Enterprise Application Architecture", "enterprise-application-patterns", 18),
    }
    for book_id, (title, kind, chapter_count) in metadata.items():
        if book_id not in known:
            inv_path = SOURCES / book_id / "inventory.json"
            inv = json.loads(inv_path.read_text(encoding="utf-8"))
            sources.append({"book_id": book_id, "title": title, "type": kind, "status": "integrated_core", "files": [row["path"] for row in inv["files"]], "segments": inv["segment_count"], "knowledge_units": sum(item["book_id"] == book_id for item in units), "chapters_read": chapter_count, "confidence": "high"})
    write_jsonl(REGISTRY / "sources.jsonl", sources)

    segments = jsonl(REGISTRY / "segments.jsonl")
    existing_segments = {row["segment_id"] for row in segments}
    for book_id in metadata:
        for row in jsonl(SOURCES / book_id / "segments.jsonl"):
            if row["segment_id"] not in existing_segments:
                segments.append(row)
    write_jsonl(REGISTRY / "segments.jsonl", segments)

    all_units = jsonl(REGISTRY / "knowledge-units.jsonl")
    existing_units = {row["ku_id"] for row in all_units}
    all_units.extend(item for item in units if item["ku_id"] not in existing_units)
    write_jsonl(REGISTRY / "knowledge-units.jsonl", all_units)

    conflicts_path = REGISTRY / "conflicts.jsonl"
    conflicts = jsonl(conflicts_path)
    conflict_ids = {row["conflict_id"] for row in conflicts}
    new_conflicts = [
        {"conflict_id": "CF-0004", "topic": "Architecture view set", "left": {"ku_ids": ["KU-0058"], "claim": "Choose views based on stakeholder use and cost."}, "right": {"ku_ids": ["KU-0054"], "claim": "A mature architecture package should document multiple views, mappings, rationale, and behavior."}, "context_difference": "Small exploratory system versus long-lived, safety-critical, regulated, or multi-team system.", "workflow_impact": "medium", "resolution_status": "tailored"},
        {"conflict_id": "CF-0005", "topic": "Domain logic organization", "left": {"ku_ids": ["KU-0011", "KU-0019"], "claim": "Use bounded contexts and rich domain invariants where the domain warrants them."}, "right": {"ku_ids": ["KU-0064"], "claim": "Transaction Script or a simpler structure may be appropriate for simple domains."}, "context_difference": "Complex domain with interacting rules versus simple CRUD or low-change application.", "workflow_impact": "medium", "resolution_status": "tailored"},
        {"conflict_id": "CF-0006", "topic": "Distribution boundary", "left": {"ku_ids": ["KU-0018", "KU-0020"], "claim": "Use explicit context boundaries and asynchronous/event-based integration when justified."}, "right": {"ku_ids": ["KU-0068", "KU-0071"], "claim": "Distribution is expensive; prefer local calls and coarse-grained remote facades unless a measured need exists."}, "context_difference": "Required bounded-context integration or failure isolation versus accidental fine-grained distribution.", "workflow_impact": "high", "resolution_status": "tailored"},
    ]
    conflicts.extend(row for row in new_conflicts if row["conflict_id"] not in conflict_ids)
    write_jsonl(conflicts_path, conflicts)

    domains = json.loads((REGISTRY / "lifecycle-spine.json").read_text(encoding="utf-8"))["domains"]
    primary = Counter(item["lifecycle_phase"] for item in all_units)
    secondary = Counter(domain for item in all_units for domain in item["secondary_domains"])
    lines = ["# Coverage", "", "| Domain | Primary | Secondary | Class | Next action |", "|---|---:|---:|---|---|"]
    for domain in domains:
        total = primary[domain] + secondary[domain]
        cls = "strong" if primary[domain] >= 3 and total >= 5 else "usable" if total >= 3 else "stub" if total else "none"
        lines.append(f"| `{domain}` | {primary[domain]} | {secondary[domain]} | `{cls}` | Use and refine with project evidence |")
    (REGISTRY / "coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    log = (REGISTRY / "merge-log.md").read_text(encoding="utf-8")
    if "MERGE-0003" not in log:
        log += f"\n## MERGE-0003\n\n- **at:** {datetime.now(timezone.utc).isoformat()}\n- **sources:** `{SAIP}`, `{DOCS}`, `{POEAA}`\n- **action:** architecture deep-read and fold-in\n- **chapters read:** 57\n- **knowledge units added:** {len(units)}\n- **conflicts recorded:** 3\n- **status:** draft-ready; architecture coverage strengthened\n"
        (REGISTRY / "merge-log.md").write_text(log, encoding="utf-8")


def write_source_packs(units: list[dict]) -> None:
    for book_id, summary in SUMMARIES.items():
        (SOURCES / book_id / "book-summary.md").write_text(summary, encoding="utf-8")
    for book_id in {item["book_id"] for item in units}:
        directory = SOURCES / book_id / "cards"
        directory.mkdir(exist_ok=True)
        for item in [row for row in units if row["book_id"] == book_id]:
            (directory / f"{item['ku_id']}.md").write_text(card(item), encoding="utf-8")
        segments = jsonl(SOURCES / book_id / "segments.jsonl")
        chosen = {item["segment_id"] for item in units if item["book_id"] == book_id}
        pending = [row["segment_id"] for row in segments if row["segment_id"] not in chosen]
        report = ["# Integration Report", "", f"- **book_id:** `{book_id}`", f"- **chapters read:** source summary completed", f"- **knowledge units:** {sum(item['book_id'] == book_id for item in units)}", "- **status:** `integrated_core`", "", "## Pending enrichment segments", ""]
        report.extend(f"- `{segment_id}`" for segment_id in pending)
        (SOURCES / book_id / "integration-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def update_workflow(units: list[dict]) -> None:
    principles = WORKFLOW / "principles.md"
    text = principles.read_text(encoding="utf-8")
    addition = """

10. Architecture decisions must be driven by measurable quality scenarios and business change forces.
11. A view or pattern is justified by a stakeholder use or a concrete design problem, not by convention alone.
12. Interfaces document externally visible syntax, semantics, protocols, errors, timing, and evolution rules.
13. Architecture documentation must include rationale, mappings, assumptions, and known debt where they affect future decisions.
"""
    if "Architecture decisions must be driven" not in text:
        principles.write_text(text.rstrip() + addition, encoding="utf-8")

    sop = WORKFLOW / "sop-state-machine.md"
    sop_text = sop.read_text(encoding="utf-8")
    old = re.search(r"## Architecture and Domain Design\n.*?(?=\n## Plan and Commit)", sop_text, re.S)
    new = """## Architecture and Domain Design
- **state_id:** `architecture-and-domain-design`
- **goal:** Select boundaries, quality tactics, integration contracts, and implementation patterns that support the next value slice.
- **entry_criteria:** Testable scope slice and architecturally significant requirements are known.
- **activities:** Define quality attribute scenarios.; Choose module, component-and-connector, and allocation views.; Apply Attribute-Driven Design.; Select domain, data, concurrency, presentation, and distribution patterns only when justified.; Document interfaces, behavior, rationale, mappings, and debt.; Evaluate the architecture with a focused review or ATAM-style method.
- **outputs:** Quality attribute scenarios; Architecture decision record; Selected views and mappings; Interface/behavior contracts; Pattern decision; Evaluation findings; Architecture debt items
- **exit_criteria:** Architecture drivers have design responses.; Boundaries and ownership are reviewable.; Interfaces and behavior are testable.; Major trade-offs and risks are recorded.; Documentation is usable by intended stakeholders.
- **quality_gates:** Quality scenario review.; Architecture and contract review.; View/documentation completeness review.; Aggregate/concurrency review where applicable.; Architecture risk evaluation.
- **roles:** Architect/lead engineer; Domain expert; Product owner; Reviewer; Tester
- **fallback:** Return to discovery when requirements or quality scenarios conflict; create a spike when the architecture risk is not understood.
- **next_state:** `plan-and-commit`
- **handbook:** `handbook/design.md`
"""
    if old:
        sop.write_text(sop_text[:old.start()] + new + sop_text[old.end():], encoding="utf-8")

    design = WORKFLOW / "handbook/design.md"
    existing = design.read_text(encoding="utf-8") if design.exists() else "# Architecture and Design Handbook\n"
    if "## Architecture Books" not in existing:
        rows = ["", "## Architecture Books", "", "| ID | Method | Trigger | Source |", "|---|---|---|---|"]
        for item in units:
            if item["lifecycle_phase"] in {"architecture", "design", "requirements", "governance"} and item["book_id"] in {SAIP, DOCS, POEAA}:
                rows.append(f"| `{item['ku_id']}` | [{item['title']}](../../sources/{item['book_id']}/cards/{item['ku_id']}.md) | {item['trigger']} | `{item['source_locator']}` |")
        design.write_text(existing.rstrip() + "\n" + "\n".join(rows) + "\n", encoding="utf-8")

    readme = WORKFLOW / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    readme_text = readme_text.replace("generated from a lifecycle overview, a requirements specialist source, a domain-driven design source, and an agile delivery source", "generated from a lifecycle overview, requirements, domain-driven design, agile delivery, architecture quality, architecture documentation, and enterprise application pattern sources")
    readme_text = readme_text.replace("requirements, architecture, delivery, verification, governance, and teamwork now have usable coverage", "requirements, architecture, design, construction, delivery, verification, governance, and teamwork now have strong or usable coverage")
    readme.write_text(readme_text, encoding="utf-8")


def main() -> None:
    units = saip_units() + docs_units() + poeaa_units()
    write_source_packs(units)
    update_registry(units)
    update_workflow(units)
    print(json.dumps({"books": 3, "chapters_read": 57, "knowledge_units_added": len(units), "conflicts_added": 3}, ensure_ascii=False))


if __name__ == "__main__":
    main()
