"""Fold the workflow-relevant findings from the three remaining books into Workflow B."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("work/se-workflow")
REGISTRY = ROOT / "registry"
SOURCES = ROOT / "sources"
WORKFLOW = ROOT / "workflow-b"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def segment(book_id: str, start_line: int) -> dict:
    rows = read_jsonl(SOURCES / book_id / "segments.jsonl")
    return next(row for row in rows if row["start_line"] <= start_line <= row["end_line"])


def unit(
    number: int,
    book_id: str,
    start_line: int,
    title: str,
    domain: str,
    kind: str,
    purpose: str,
    trigger: str,
    procedure: list[str],
    checks: list[str],
    tailoring: dict,
    anti_patterns: list[str],
    secondary: list[str] | None = None,
    merge_status: str = "NEW",
) -> dict:
    source = segment(book_id, start_line)
    return {
        "ku_id": f"KU-{number:04d}",
        "segment_id": source["segment_id"],
        "book_id": book_id,
        "title": title,
        "lifecycle_phase": domain,
        "secondary_domains": secondary or [],
        "knowledge_type": kind,
        "confidence": "high",
        "merge_status": merge_status,
        "needs_review": False,
        "status": "integrated_core",
        "purpose": purpose,
        "trigger": trigger,
        "inputs": ["Relevant stakeholder evidence", "Current project context"],
        "outputs": ["Recorded decision or work product", "Objective review evidence"],
        "procedure": procedure,
        "checks": checks,
        "anti_patterns": anti_patterns,
        "tailoring": tailoring,
        "source_locator": source["source_locator"],
    }


def card_markdown(item: dict) -> str:
    lines = [
        f"# {item['ku_id']}: {item['title']}",
        "",
        f"- **book_id:** `{item['book_id']}`",
        f"- **segment_id:** `{item['segment_id']}`",
        f"- **lifecycle_phase:** `{item['lifecycle_phase']}`",
        f"- **knowledge_type:** `{item['knowledge_type']}`",
        f"- **merge_status:** `{item['merge_status']}`",
        "",
        "## Purpose",
        item["purpose"],
        "",
        "## Trigger",
        item["trigger"],
        "",
        "## Procedure",
    ]
    lines.extend(f"{number}. {step}" for number, step in enumerate(item["procedure"], 1))
    lines.extend(["", "## Checks"])
    lines.extend(f"- {check}" for check in item["checks"])
    lines.extend(["", "## Anti-patterns"])
    lines.extend(f"- {pattern}" for pattern in item["anti_patterns"])
    lines.extend(["", "## Tailoring", f"`{json.dumps(item['tailoring'], ensure_ascii=False)}`", "", "## Source", f"`{item['source_locator']}`", ""])
    return "\n".join(lines)


DDD = "vernon-ddd-distilled"
AGILE = "ford-greene-nature-of-software-development"
REQ = "wiegers-beatty-software-requirements-3e"

NEW_UNITS = [
    unit(15, DDD, 226, "Bounded contexts and ubiquitous language", "architecture", "method", "Align model, team ownership, code, and terminology within an explicit semantic boundary.", "A complex domain contains terms with different meanings across business functions.", ["Identify competing meanings in business language.", "Draw a bounded-context boundary around one coherent model.", "Define the team's ubiquitous language with domain experts.", "Assign clear ownership and public interfaces."], ["Each cross-context term has a defined local meaning.", "The boundary has an owning team and published integration contract."], {"light": "Name one domain boundary and maintain a glossary.", "heavy": "Context map, ownership model, separate repositories, and acceptance tests.", "cannot_remove": False}, ["Letting one model accumulate incompatible business meanings."], ["requirements", "teamwork", "governance"]),
    unit(16, DDD, 564, "Core, supporting, and generic subdomains", "problem-framing", "decision_rule", "Focus scarce expert effort on the domain that differentiates the business.", "Deciding where to invest custom design, product ownership, or specialist expertise.", ["Inventory subdomains.", "Classify each as core, supporting, or generic.", "Allocate strongest people and bespoke investment to the core domain.", "Buy, reuse, or simplify generic concerns when prudent."], ["Core-domain rationale is explicit.", "Investment level matches strategic importance."], {"light": "Classify major product areas during inception.", "heavy": "Maintain a subdomain portfolio with investment and sourcing decisions.", "cannot_remove": False}, ["Applying equal bespoke-design effort to every subsystem."], ["planning", "architecture"]),
    unit(17, DDD, 748, "Context mapping and integration relationships", "architecture", "method", "Choose inter-team and technical integration relationships deliberately rather than allowing accidental coupling.", "Two bounded contexts need to exchange behavior or information.", ["Map upstream and downstream contexts.", "Choose a relationship such as partnership, customer-supplier, shared kernel, conformist, or separate ways.", "Document ownership, service expectations, and change coordination.", "Review the relationship as costs and dependencies evolve."], ["Every integration has an owner, direction, and change policy.", "The mapping explains both team and technical coupling."], {"light": "Record supplier, consumer, and interface owner in the ADR.", "heavy": "Versioned context map with service-level and dependency reviews.", "cannot_remove": True}, ["Treating every API edge as a purely technical choice."], ["teamwork", "governance"]),
    unit(18, DDD, 748, "Anti-corruption layer and published integration language", "architecture", "method", "Protect a local model from foreign or legacy concepts while supplying stable consumer-oriented contracts.", "Integrating with legacy, external, or differently modeled systems.", ["Define the consumer's required language and use cases.", "Translate external data at an anti-corruption boundary.", "Expose documented published schemas and an open host service where owning the provider.", "Avoid exposing aggregate internals as an API."], ["Consumers do not import provider domain types.", "API resources and events satisfy consumer use cases, not internal storage shape."], {"light": "Adapter at each external integration point.", "heavy": "Versioned published language, compatibility policy, and contract tests.", "cannot_remove": True}, ["Direct database sharing or letting a provider model leak across the boundary."], ["construction", "governance"], "EXTENDS"),
    unit(19, DDD, 1031, "Aggregate consistency boundaries", "design", "method", "Model transactional consistency around business invariants while keeping change units small and testable.", "Defining domain objects that carry business rules or deciding transactional scope.", ["Identify the business invariant that must hold after one operation.", "Place only the necessary entities and values inside the aggregate boundary.", "Keep aggregates small and reference other aggregates by identity.", "Use separate transactions for other aggregates."], ["Every aggregate has a stated invariant.", "No transaction changes unrelated aggregates without a deliberate consistency decision."], {"light": "State invariants and boundary in an ADR or model sketch.", "heavy": "Aggregate tests, concurrency tests, and transaction design review.", "cannot_remove": False}, ["Large object clusters that couple unrelated lifecycle changes."], ["architecture", "construction", "verification"]),
    unit(20, DDD, 1378, "Domain events and eventual consistency", "architecture", "method", "Publish business-significant past occurrences to coordinate changes across boundaries without synchronous coupling.", "A state change must inform another aggregate or bounded context.", ["Name the event in past tense using ubiquitous language.", "Include the event's essential business facts and occurrence metadata.", "Persist the aggregate update and event atomically.", "Publish through a versioned schema.", "Make consumers idempotent and handle causal ordering."], ["Events describe a fact, not a command.", "Consumer retry cannot duplicate a business effect.", "Event ordering requirements are explicit."], {"light": "Local domain-event dispatch with deduplication tests.", "heavy": "Transactional outbox/event store, schema governance, delivery monitoring, and replay strategy.", "cannot_remove": False}, ["Blocking chains of synchronous service calls or publishing ambiguous `Updated` snapshots."], ["construction", "verification", "operations"]),
    unit(21, DDD, 1714, "Event storming, modeling spikes, and modeling debt", "requirements", "method", "Acquire domain knowledge quickly, turn uncertainty into tested scenarios, and retain unfinished modeling work as visible debt.", "Starting a complex domain, facing ambiguous workflows, or discovering a model mismatch during an iteration.", ["Run a time-boxed event-storming session with domain experts and engineers.", "Identify events, commands, aggregates, policies, and unanswered questions.", "Refine high-risk scenarios with domain experts.", "Create acceptance tests or executable specifications.", "Record unresolved model work as modeling debt and schedule it."], ["Domain experts review critical scenarios and acceptance tests.", "Unresolved model questions have an owner and backlog item."], {"light": "One-hour mapping session before a risky story.", "heavy": "Multi-day inception, context map, scenario suite, and scheduled modeling debt review.", "cannot_remove": False}, ["Treating task-board movement as sufficient design discovery."], ["risk", "planning", "verification"]),
    unit(22, AGILE, 260, "Value-first feature slicing and release planning", "planning", "method", "Deliver value and learning earlier by selecting small user-visible features before lower-value scope.", "A product has more desired work than time or budget permits.", ["State the value sought by each candidate feature.", "Split features into independently valuable slices.", "Order slices by value, urgency, cost, and learning.", "Release the smallest useful subset early.", "Stop or redirect investment when marginal value falls."], ["Every planned item names user or business value.", "A release contains demonstrable user-facing capability."], {"light": "Prioritized feature list with a demo every iteration.", "heavy": "Portfolio decision records, value hypotheses, and release experiments.", "cannot_remove": True}, ["Phase completion reported as value delivery."], ["problem-framing", "feedback", "release"], "EXTENDS"),
    unit(23, AGILE, 611, "Rolling feature planning", "planning", "method", "Steer scope at a short cadence instead of pretending a distant detailed plan is reliable.", "Iterative work with uncertainty, changing evidence, or a fixed time and budget envelope.", ["Set the time and funding boundary.", "Keep a prioritized feature backlog.", "Split stories into small business-recognizable slices.", "Let the team select feasible work using recent delivery evidence.", "Replan before each iteration and remove excess work early."], ["The iteration commitment is based on evidence, not stretch pressure.", "Deferred work remains visible without being treated as failure."], {"light": "Weekly backlog refinement and a two-week planning horizon.", "heavy": "Rolling forecast with release scenarios and capacity history.", "cannot_remove": False}, ["Detailed long-range task plans treated as commitments; stretch goals that trade away quality."], ["requirements", "risk"], "CONTRADICTS"),
    unit(24, AGILE, 746, "Potentially shippable vertical increments", "construction", "method", "Treat a feature as done only when its requirements, design, implementation, and verification form a working product slice.", "Planning or reporting work inside a short delivery cadence.", ["Choose a thin feature with clear business behavior.", "Define the acceptance evidence before building.", "Complete analysis, design, code, integration, and tests within the iteration.", "Demonstrate the running feature.", "Do not carry hidden test-and-fix work as done."], ["Done means running and verified, not partially coded.", "The product is releasable at iteration end."], {"light": "One end-to-end scenario per feature.", "heavy": "Release-quality evidence for every vertical slice.", "cannot_remove": True}, ["Using percent-complete as a substitute for a working increment."], ["requirements", "verification", "release"], "EXTENDS"),
    unit(25, AGILE, 866, "Features and foundation in parallel", "architecture", "method", "Grow the minimum viable product and its supporting design together, avoiding both infrastructure-first and feature-polish-first waste.", "A product needs architectural investment while value delivery is urgent.", ["Identify the smallest useful versions of the key features.", "Build only the enabling foundation needed by the next slices.", "Refine feature capability and foundation in successive iterations.", "Inspect the running product and adjust investment."], ["Foundation work has a named feature or risk it enables.", "The product remains valuable and shippable throughout."], {"light": "Architecture spikes tied to the next feature.", "heavy": "Architecture runway, capability roadmap, and enabling-work review.", "cannot_remove": True}, ["Completing architecture before exposing any user value."], ["planning", "construction", "release"], "EXTENDS"),
    unit(26, AGILE, 974, "Automated acceptance tests, TDD, and refactoring", "verification", "method", "Maintain reliable delivery speed through two layers of automated tests and continuous design improvement.", "Any iterative product whose changes must remain safe and affordable.", ["Define business-level acceptance tests for each feature.", "Automate regression checks for accepted behavior.", "Use developer-level tests to expose design errors quickly.", "Refactor continuously while tests protect behavior.", "Repair defects immediately rather than accumulating a late test-and-fix phase."], ["New behavior has business acceptance evidence.", "Developer checks run frequently.", "Refactoring leaves behavior intact."], {"light": "Automated critical-path acceptance tests plus unit tests for changed code.", "heavy": "Continuous test pipeline, quality thresholds, and design-debt budget.", "cannot_remove": True}, ["Deferring comprehensive tests and design cleanup to a stabilization phase."], ["construction", "quality", "release"], "EXTENDS"),
    unit(27, AGILE, 1768, "Feature teams and shared regression checks", "teamwork", "method", "Scale delivery by organizing around end-to-end features and using a shared automated test suite as the coordination mechanism.", "More than one team must deliver to a common product.", ["Establish cross-functional feature teams.", "Integrate small changes frequently into the common product.", "Run the shared automated checks before and after integration.", "Fix failures introduced by the change before proceeding.", "Add specialist infrastructure support only where feature teams cannot own it."], ["Every team can deliver an end-to-end feature.", "The common codebase remains green."], {"light": "One pilot feature team and shared CI checks.", "heavy": "Multiple feature teams, trunk-based integration, and explicit cross-team dependency practices.", "cannot_remove": False}, ["Sequential functional handoffs and separately green component branches."], ["construction", "verification", "governance"], "EXTENDS"),
    unit(28, REQ, 1948, "Business vision, scope, and measurable success", "problem-framing", "artifact", "Anchor product decisions in business opportunity, objectives, scope boundaries, and observable success measures.", "Starting a product, release, or major enhancement.", ["Identify the business problem or opportunity.", "Write measurable business objectives and success criteria.", "Define product vision and the current project or iteration scope.", "Record exclusions, constraints, stakeholders, and business risks.", "Use the document to screen proposed scope changes."], ["Each requested feature can be related to an objective or justified exclusion.", "Vision remains stable while near-term scope can change deliberately."], {"light": "One-page vision and scope statement.", "heavy": "Approved vision-and-scope document with success metrics and stakeholder profiles.", "cannot_remove": True}, ["Treating a requested solution as a business objective."], ["requirements", "planning", "risk"], "EXTENDS"),
    unit(29, REQ, 2423, "Stakeholder and user-class analysis", "requirements", "method", "Ensure requirements come from relevant user classes, customers, sponsors, and other affected stakeholders.", "A project has multiple user roles, indirect users, or conflicting viewpoints.", ["Identify stakeholder and user classes.", "Describe their characteristics, goals, authority, and availability.", "Select representative participants for elicitation and review.", "Resolve representation gaps before baselining."], ["Every significant user class has a known representative or documented gap.", "Decision authority is explicit."], {"light": "Stakeholder map and one representative per key user class.", "heavy": "User-class profiles, RACI, and participation plan.", "cannot_remove": True}, ["Assuming a sponsor or developer speaks for all users."], ["teamwork", "problem-framing"], "EXTENDS"),
    unit(30, REQ, 2774, "Collaborative requirements elicitation", "requirements", "method", "Discover needs through structured conversations, workshops, scenarios, document analysis, and interface analysis.", "Requirements are incomplete, disputed, or based on assumptions.", ["Prepare goals, scope, participants, and questions.", "Use interviews, workshops, observation, document analysis, or interface analysis.", "Elicit scenarios, exceptions, constraints, and business rules.", "Record decisions, open issues, and follow-up owners.", "Review findings with participants."], ["Each session has a goal and output.", "Open issues have owners and dates."], {"light": "Focused interview or story-mapping session.", "heavy": "Facilitated cross-stakeholder workshop series with evidence repository.", "cannot_remove": True}, ["Asking only 'what do you want?' or treating a single interview as complete discovery."], ["teamwork", "risk"], "EXTENDS"),
    unit(31, REQ, 3478, "Business-rule catalog and traceability", "requirements", "artifact", "Manage policy, constraint, trigger, inference, and calculation rules as reusable business assets rather than copying them into features.", "Rules affect multiple requirements, products, or regulatory obligations.", ["Identify the rule and its business source.", "Classify it and record it atomically with a stable ID.", "Validate whether it is current and applicable.", "Trace implementing requirements and tests to the rule ID.", "Review rule changes for downstream impact."], ["Rules have owners, sources, and applicability.", "No duplicated rule text silently diverges across specifications."], {"light": "Rule table with identifiers and linked requirement cards.", "heavy": "Enterprise rule repository, decision tables, and governed change process.", "cannot_remove": False}, ["Hard-coding volatile policy or combining multiple rules into one opaque statement."], ["governance", "design", "verification"], "NEW"),
    unit(32, REQ, 363, "Clear and testable requirements", "requirements", "checklist", "Write requirements and requirement sets that are complete, correct, feasible, necessary, unambiguous, prioritized, verifiable, modifiable, and traceable.", "Documenting a functional, quality, data, or constraint requirement.", ["Use a consistent requirement form.", "State one observable behavior or constraint.", "Eliminate vague and subjective terms.", "Identify source, rationale, priority, and verification method.", "Review the set for completeness, consistency, modifiability, and traceability."], ["A tester can derive an acceptance check without guessing.", "A change can identify affected linked artifacts."], {"light": "Definition-of-ready checklist on each story.", "heavy": "Formal SRS quality inspection and traceability audit.", "cannot_remove": True}, ["Compound statements, ambiguous adjectives, and untestable aspirations."], ["verification", "quality"], "EXTENDS"),
    unit(33, REQ, 707, "Requirements modeling", "requirements", "method", "Use visual models to reveal missing behavior, decisions, data, states, and handoffs that prose hides.", "Text requirements contain complex workflows, decisions, data relationships, or stateful behavior.", ["Select a model suited to the question: data flow, swimlane, state, dialog, decision table/tree, or event-response.", "Model the problem rather than an assumed implementation.", "Review the model with stakeholders.", "Link model elements to narrative requirements and tests."], ["The model resolves a documented ambiguity or omission.", "Stakeholders can validate model behavior."], {"light": "One workflow or state model for high-risk behavior.", "heavy": "Linked analysis-model suite with formal review.", "cannot_remove": False}, ["Creating diagrams that restate implementation choices without clarifying the problem."], ["design", "verification"], "EXTENDS"),
    unit(34, REQ, 1051, "Quantified quality attributes and constraints", "requirements", "method", "Turn quality attributes into ranked, measurable, testable requirements with explicit trade-offs.", "A system has performance, reliability, security, usability, interoperability, scalability, or other quality concerns.", ["Start with a broad attribute taxonomy.", "Trim to relevant attributes and rank their importance.", "Elicit concrete scenarios and measures for each priority attribute.", "Write measurable quality requirements and constraints.", "Analyze trade-offs and trace them to architecture and tests."], ["Every priority quality attribute has a measurable condition and verification method.", "Conflicting attributes have a recorded trade-off decision."], {"light": "Top three quality scenarios with target measures.", "heavy": "Quality attribute workshop, scenario catalog, architecture evaluation, and test plan.", "cannot_remove": True}, ["Writing 'fast', 'secure', or 'user friendly' without a measurable context."], ["architecture", "verification", "risk"], "EXTENDS"),
    unit(35, REQ, 2097, "Risk-reducing prototypes", "risk", "method", "Use disposable or evolutionary prototypes deliberately to reduce requirement, UX, feasibility, and technical uncertainty.", "A decision is expensive, ambiguous, novel, or hard to validate through discussion alone.", ["State the question and risk the prototype will address.", "Choose paper, electronic, proof-of-concept, throwaway, or evolutionary form.", "Define an evaluation script and participants.", "Run the evaluation and record the decision.", "Dispose of throwaway code or explicitly requalify it before production use."], ["Prototype outcome changes a decision, requirement, or risk rating.", "Stakeholders understand whether the prototype is production-bound."], {"light": "Paper prototype or short spike with explicit question.", "heavy": "Instrumented usability or technical prototype with evaluation report.", "cannot_remove": False}, ["Shipping prototype code merely because it already exists."], ["requirements", "architecture", "verification"], "EXTENDS"),
    unit(36, REQ, 2438, "Value, cost, and risk-based prioritization", "planning", "decision_rule", "Allocate constrained delivery capacity by making trade-offs visible across value, cost, risk, and urgency.", "Selecting a release, iteration, or change request.", ["Define the decision criteria with stakeholders.", "Estimate relative value, cost, risk, and dependency.", "Apply a suitable technique such as pairwise comparison, three-level grouping, or weighted scoring.", "Assign selected work to a release or iteration.", "Revisit priority when evidence or constraints change."], ["Priority has a recorded rationale.", "The team can explain what was deferred and why."], {"light": "Must/should/could with an explicit decision owner.", "heavy": "Multi-factor scoring and release scenario analysis.", "cannot_remove": True}, ["Declaring every requested item highest priority."], ["requirements", "risk"], "EXTENDS"),
    unit(37, REQ, 2823, "Requirements validation through review and acceptance criteria", "verification", "method", "Validate requirements before costly implementation by reviewing them with customers, developers, and testers and deriving acceptance evidence.", "A requirement set is ready for baseline, iteration commitment, or implementation.", ["Prepare requirements, models, and acceptance conditions.", "Inspect for correctness, completeness, consistency, feasibility, necessity, and testability.", "Review with representative stakeholders, developers, and testers.", "Resolve findings or record a risk decision.", "Approve the validated subset."], ["Every accepted requirement has acceptance evidence.", "Unresolved disputes have a decision owner and date."], {"light": "Scenario walkthrough and acceptance-criteria review.", "heavy": "Formal inspection with defect log and approval record.", "cannot_remove": True}, ["Treating a document handoff as evidence of shared understanding."], ["quality", "teamwork"], "EXTENDS"),
    unit(38, REQ, 3452, "Just-in-time requirements for agile delivery", "requirements", "method", "Keep early agile requirements lightweight while progressively elaborating the next work slice with acceptance evidence.", "An exploratory or iterative project uses a product backlog and short delivery cycles.", ["Capture high-level needs as backlog items.", "Prioritize them by product value and risk.", "Elaborate the next iteration's stories with the team and user representative.", "Add acceptance criteria and necessary models before commitment.", "Retain traceability proportionate to risk."], ["Near-term stories are understood and testable before implementation.", "Future work remains intentionally less detailed."], {"light": "Story plus examples and acceptance criteria.", "heavy": "Backlog linked to vision, architecture, tests, and regulated traceability.", "cannot_remove": True}, ["Mistaking agile for skipping elicitation, validation, or governance."], ["planning", "verification"], "CONTRADICTS"),
    unit(39, REQ, 352, "Requirements baselines, attributes, and status", "governance", "method", "Maintain an agreed requirement set through baselines, version control, stable identifiers, attributes, and lifecycle status.", "Requirements are approved for a release, iteration, contract, or downstream implementation.", ["Review and approve the selected requirement subset.", "Create a named baseline and version.", "Assign stable identifiers and essential attributes.", "Track status from proposed through verified, deferred, deleted, or rejected.", "Communicate the current version to all affected roles."], ["Every implementation target maps to one current baseline.", "Reported progress is based on requirement status, not guessed percentage."], {"light": "Approved iteration backlog with stable IDs and status board.", "heavy": "SRS/RM repository, baselines, version history, and release status reports.", "cannot_remove": True}, ["Multiple authoritative versions of an SRS or scope drifting without a baseline."], ["requirements", "planning", "release"], "EXTENDS"),
    unit(40, REQ, 971, "Change control and impact analysis", "governance", "method", "Evaluate, decide, implement, verify, and communicate requirement changes without silently breaking commitments.", "A new requirement, changed requirement, or removed requirement affects an approved baseline.", ["Log the request with rationale and source.", "Check scope alignment and analyze impacts on requirements, design, tests, schedule, cost, risk, and commitments.", "Have the authorized decision maker accept, reject, defer, or request more analysis.", "Implement and verify accepted changes.", "Update baselines, links, status, and stakeholder communication."], ["Every baseline change has a recorded decision and impact.", "Commitment changes are renegotiated rather than hidden."], {"light": "Product owner decision plus linked impact note.", "heavy": "CCB charter, defined request states, impact template, and status reporting.", "cannot_remove": True}, ["Freezing needs informally while accepting untracked side-channel changes."], ["requirements", "risk", "planning"], "EXTENDS"),
    unit(41, REQ, 1309, "End-to-end requirements traceability", "governance", "method", "Maintain links from business objectives and rules through requirements, design, code, tests, releases, and changes.", "The project is high-risk, regulated, long-lived, multi-team, or needs reliable change impact analysis.", ["Choose traceability depth based on risk and cost.", "Define link types and owners.", "Create links from requirements to source, design, implementation, and verification artifacts.", "Use links during impact analysis and release readiness.", "Audit stale or missing links periodically."], ["Every high-risk or regulated requirement has implementation and verification evidence.", "Links support an actual impact or coverage query."], {"light": "Requirement-to-acceptance-test links for committed scope.", "heavy": "Traceability matrix or RM tool across the full lifecycle.", "cannot_remove": False}, ["Creating a large trace matrix that nobody uses to make decisions."], ["verification", "release", "maintenance"], "NEW"),
    unit(42, REQ, 1670, "Requirements risk management and process improvement", "risk", "method", "Treat requirement uncertainty, participation gaps, ambiguity, scope growth, and unmanaged change as risks with explicit mitigation and learning.", "A team has recurring requirement failures or starts a project with material uncertainty.", ["Assess current practice and identify a small number of pain points.", "Identify requirement-specific risks, probability, impact, triggers, and owners.", "Select targeted process changes and pilot them.", "Measure outcomes and adjust incrementally.", "Escalate unmanaged high-exposure risks."], ["Risks distinguish future uncertainty from current issues.", "Improvement work has measurable objectives and an owner."], {"light": "Top requirement risks and one improvement experiment.", "heavy": "Organizational assessment, roadmap, training, metrics, and periodic audit.", "cannot_remove": True}, ["Adopting a large process change without a specific pain point or feedback loop."], ["requirements", "quality", "planning", "feedback"], "EXTENDS"),
]


def write_source_pack_reports() -> None:
    grouped = Counter(item["book_id"] for item in NEW_UNITS)
    for book_id, count in grouped.items():
        pack = SOURCES / book_id
        items = [item for item in NEW_UNITS if item["book_id"] == book_id]
        card_dir = pack / "cards"
        card_dir.mkdir(exist_ok=True)
        for item in items:
            (card_dir / f"{item['ku_id']}.md").write_text(card_markdown(item), encoding="utf-8")
        all_segments = read_jsonl(pack / "segments.jsonl")
        processed = {item["segment_id"] for item in items}
        pending = [row["segment_id"] for row in all_segments if row["segment_id"] not in processed]
        report = [
            "# Integration Report",
            "",
            f"- **book_id:** `{book_id}`",
            f"- **knowledge units:** {count}",
            "- **status:** `integrated_core`",
            "- **scope:** Workflow-relevant deep extraction; unselected segments remain available for topic-specific enrichment.",
            "",
            "## Added Knowledge Units",
            "",
        ]
        report.extend(f"- `{item['ku_id']}` {item['title']} ({item['merge_status']})" for item in items)
        report.extend(["", "## Pending Non-Core Segments", ""])
        report.extend(f"- `{segment_id}`" for segment_id in pending)
        (pack / "integration-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def update_registry() -> None:
    sources = read_jsonl(REGISTRY / "sources.jsonl")
    known_sources = {row["book_id"] for row in sources}
    source_metadata = {
        DDD: ("Domain-Driven Design Distilled", "architecture-and-domain-modeling"),
        AGILE: ("The Nature of Software Development", "agile-and-continuous-delivery"),
        REQ: ("Software Requirements, 3rd Edition", "requirements-specialist"),
    }
    for book_id, (title, source_type) in source_metadata.items():
        if book_id not in known_sources:
            inventory = json.loads((SOURCES / book_id / "inventory.json").read_text(encoding="utf-8"))
            sources.append({"book_id": book_id, "title": title, "type": source_type, "status": "integrated_core", "files": [row["path"] for row in inventory["files"]], "segments": inventory["segment_count"], "knowledge_units": sum(item["book_id"] == book_id for item in NEW_UNITS), "confidence": "high"})
    write_jsonl(REGISTRY / "sources.jsonl", sources)

    segments = read_jsonl(REGISTRY / "segments.jsonl")
    known_segment_ids = {row["segment_id"] for row in segments}
    for book_id in source_metadata:
        for row in read_jsonl(SOURCES / book_id / "segments.jsonl"):
            if row["segment_id"] not in known_segment_ids:
                segments.append(row)
    write_jsonl(REGISTRY / "segments.jsonl", segments)

    units = read_jsonl(REGISTRY / "knowledge-units.jsonl")
    known_unit_ids = {row["ku_id"] for row in units}
    units.extend(item for item in NEW_UNITS if item["ku_id"] not in known_unit_ids)
    write_jsonl(REGISTRY / "knowledge-units.jsonl", units)

    conflicts = read_jsonl(REGISTRY / "conflicts.jsonl")
    conflict_ids = {row["conflict_id"] for row in conflicts}
    new_conflicts = [
        {"conflict_id": "CF-0001", "topic": "Planning precision", "left": {"ku_ids": ["KU-0004"], "claim": "Use decomposition and empirical estimation for plans."}, "right": {"ku_ids": ["KU-0023"], "claim": "Use rolling value-based planning and avoid detailed distant estimates."}, "context_difference": "Contractual or high-assurance planning versus exploratory iterative delivery.", "workflow_impact": "medium", "resolution_status": "tailored"},
        {"conflict_id": "CF-0002", "topic": "Requirements baseline timing", "left": {"ku_ids": ["KU-0039", "KU-0040"], "claim": "Approved scope is controlled through a baseline and change process."}, "right": {"ku_ids": ["KU-0038"], "claim": "Future agile work remains intentionally less detailed until near-term refinement."}, "context_difference": "Regulated or contractual scope versus agile backlog elaboration.", "workflow_impact": "high", "resolution_status": "tailored"},
        {"conflict_id": "CF-0003", "topic": "Team and code ownership", "left": {"ku_ids": ["KU-0015"], "claim": "One team owns one bounded context and its model."}, "right": {"ku_ids": ["KU-0027"], "claim": "Feature teams integrate into a common product and test suite."}, "context_difference": "Independent semantic contexts versus features inside one shared product context.", "workflow_impact": "medium", "resolution_status": "tailored"},
    ]
    conflicts.extend(row for row in new_conflicts if row["conflict_id"] not in conflict_ids)
    write_jsonl(REGISTRY / "conflicts.jsonl", conflicts)

    domains = json.loads((REGISTRY / "lifecycle-spine.json").read_text(encoding="utf-8"))["domains"]
    primary = Counter(item["lifecycle_phase"] for item in units)
    secondary = Counter(domain for item in units for domain in item["secondary_domains"])
    rows = ["# Coverage", "", "| Domain | Primary | Secondary | Class | Next action |", "|---|---:|---:|---|---|"]
    for domain in domains:
        total = primary[domain] + secondary[domain]
        coverage = "strong" if primary[domain] >= 3 and total >= 5 else "usable" if total >= 3 else "stub" if total else "none"
        next_action = "Add operations specialist source" if domain == "operations" else "Deepen with targeted source" if coverage in {"stub", "none"} else "Use and refine with project evidence"
        rows.append(f"| `{domain}` | {primary[domain]} | {secondary[domain]} | `{coverage}` | {next_action} |")
    (REGISTRY / "coverage.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

    log = (REGISTRY / "merge-log.md").read_text(encoding="utf-8")
    if "MERGE-0002" not in log:
        log += "\n## MERGE-0002\n\n"
        log += f"- **at:** {datetime.now(timezone.utc).isoformat()}\n"
        log += "- **sources:** `vernon-ddd-distilled`, `ford-greene-nature-of-software-development`, `wiegers-beatty-software-requirements-3e`\n"
        log += f"- **action:** incremental core fold-in\n- **knowledge units added:** {len(NEW_UNITS)}\n- **conflicts recorded:** 3\n- **status:** draft-ready; operations-specific material remains thin\n"
        (REGISTRY / "merge-log.md").write_text(log, encoding="utf-8")


def update_workflow_b() -> None:
    (WORKFLOW / "README.md").write_text("""# Workflow B\n\nThis is a multi-source engineering workflow generated from a lifecycle overview, a requirements specialist source, a domain-driven design source, and an agile delivery source.\n\n## Control Path\n\n1. Select a project profile in `project-profiles.md`.\n2. Follow the state transition conditions in `sop-state-machine.md`.\n3. Open handbook entries for methods, checklists, and source-backed tailoring.\n4. Apply conflict and tailoring rules rather than treating every method as universal.\n\n## Status\n\n`draft-ready`: requirements, architecture, delivery, verification, governance, and teamwork now have usable coverage. Operations remains intentionally thin pending an operations/SRE source.\n""", encoding="utf-8")
    (WORKFLOW / "principles.md").write_text("""# Invariant Principles\n\n1. Start from a measurable business problem, product vision, scope boundary, and success measure.\n2. Requirements must be owned, prioritized, testable, and linked to the decisions or rules that justify them.\n3. Match documentation and control weight to risk, compliance, uncertainty, and delivery cadence.\n4. A completed increment is running, verified, integrated, and potentially releasable.\n5. Keep model language, ownership, data boundaries, and integration contracts explicit.\n6. Preserve change history, baseline identity, impact analysis, and acceptance evidence.\n7. Use automated checks and refactoring to keep delivery speed from becoming quality debt.\n8. Treat requirement uncertainty, domain ambiguity, and architecture unknowns as managed risks.\n9. Use feedback from users, delivery, and operations to revise value, scope, risk, and priorities.\n""", encoding="utf-8")
    (WORKFLOW / "project-profiles.md").write_text("""# Project Profiles\n\n## Exploratory iterative product\n\nUse when user learning is rapid, compliance is low, and a small team can release frequently. Maintain a product vision, then elaborate the next small stories just in time. Use feature slices, acceptance examples, prototypes, automated checks, and a release-ready increment every iteration.\n\n## Complex domain product\n\nUse when language is ambiguous across business functions, several models must integrate, or changeability is central. Add subdomain classification, bounded contexts, a ubiquitous-language glossary, context mapping, aggregate invariants, and published integration contracts.\n\n## Contractual or high-assurance delivery\n\nUse when scope, regulation, safety, auditability, or external acceptance dominate. Baseline approved requirements, preserve version history and traceability, run impact analysis through authorized change control, specify quality attributes quantitatively, and retain objective verification evidence.\n\n## Multi-team product\n\nUse feature teams inside a shared product context when work can be delivered end-to-end through a common codebase and regression suite. Use bounded-context ownership when teams own distinct semantic models. Do not confuse either pattern with a universal organization chart.\n""", encoding="utf-8")
    (WORKFLOW / "tailoring-rules.md").write_text("""# Tailoring Rules\n\n| Concern | Exploratory iteration | Complex domain | Contractual/high-assurance | Invariant |\n|---|---|---|---|---|\n| Vision and scope | One-page vision plus near-term stories | Vision plus core-domain rationale | Approved vision/scope and success measures | Every feature has a business rationale |\n| Requirements | Stories, examples, acceptance criteria | Ubiquitous language and scenario models | Baselined SRS/RM repository | Requirements are testable |\n| Change | Product-owner decision with impact note | Context-map and contract impact review | CCB or delegated authority | Impact and decision are recorded |\n| Design | Enough design for next vertical slice | Bounded contexts, aggregates, event contracts | Reviewed architecture and quality scenarios | Quality trade-offs are explicit |\n| Delivery | Frequent potentially shippable increments | Contract tests and idempotent event consumers | Controlled builds, approvals, and traceability | Protected behavior is verified |\n| Planning | Rolling value-based selection | Modeling spikes and visible modeling debt | Range estimates, critical dependencies, contingency | Capacity and risk are visible |\n\nNever remove: decision ownership, version identity, verification of protected behavior, change communication, and a path from production evidence back to planning.\n""", encoding="utf-8")
    (WORKFLOW / "sop-state-machine.md").write_text("""# SOP State Machine\n\n## Problem Framing\n- **entry:** Opportunity, pain, regulation, or strategic initiative has an accountable sponsor.\n- **activities:** Define business problem, vision, measurable outcomes, scope, exclusions, stakeholder classes, subdomain importance, and top risks.\n- **exit:** Decision owner approves proceed, pivot, prototype, or stop; success measures and constraints are observable.\n- **fallback:** Return when new evidence invalidates value, scope, or domain assumptions.\n\n## Discovery and Requirements\n- **entry:** Problem frame and participant plan exist.\n- **activities:** Elicit scenarios, rules, data, quality attributes, user classes, interfaces, exceptions, and acceptance criteria; use prototypes or models for uncertainty.\n- **exit:** Near-term requirements are testable, prioritized, owned, and understood by users, engineers, and testers.\n- **tailoring:** Elaborate future agile work just in time; baseline contractual or high-risk scope.\n\n## Architecture and Domain Design\n- **entry:** A testable scope slice and relevant quality attributes are known.\n- **activities:** Define modules/contexts, ownership, aggregate invariants, integration mappings, API/event contracts, and quality trade-offs.\n- **exit:** The selected design supports the next slice and its risks; boundaries and contracts are reviewable.\n- **fallback:** Return to discovery when language, invariants, or quality scenarios conflict.\n\n## Plan and Commit\n- **entry:** Prioritized backlog or approved baseline is available.\n- **activities:** Select value-bearing slices, assess capacity, dependencies, risks, and changes; record scope and commitment decisions.\n- **exit:** Team has a feasible, understood, verifiable work set with explicit deferred work.\n- **fallback:** Reprioritize or renegotiate scope, date, resources, or quality; never hide the trade-off.\n\n## Construct and Integrate\n- **entry:** The next slice has acceptance evidence and required design decisions.\n- **activities:** Implement vertical slices, automated developer checks, review changes, integrate frequently, publish events safely, and update configuration identity.\n- **exit:** Integrated build is green; changes have tests, review evidence, and no unexplained contract break.\n- **fallback:** Revisit design or requirements when a slice exposes an invalid assumption.\n\n## Verify and Release\n- **entry:** A potentially shippable increment exists.\n- **activities:** Run business acceptance, regression, security/performance/recovery checks as applicable; validate traceability and release evidence; prepare rollback.\n- **exit:** Protected behavior passes, known risk is dispositioned, and the release has an accountable decision.\n- **fallback:** Return to construction, design, discovery, or planning based on defect origin.\n\n## Operate and Learn\n- **entry:** Release is accepted.\n- **activities:** Observe outcomes, defects, demand, cost, reliability, and change impact; feed evidence into value, requirements, risks, and backlog.\n- **exit:** Learning produces owned follow-up decisions.\n- **gap:** Add an operations/SRE specialist source before using this state for high-criticality operations.\n""", encoding="utf-8")

    handbook = {
        "requirements.md": ("Requirements Handbook", [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]),
        "design.md": ("Architecture and Design Handbook", [15, 16, 17, 18, 19, 20]),
        "construction.md": ("Construction Handbook", [20, 24, 25, 26, 27]),
        "testing.md": ("Verification Handbook", [24, 26, 32, 34, 37, 41]),
        "governance.md": ("Governance Handbook", [17, 18, 31, 39, 40, 41]),
        "management.md": ("Planning, Risk, and Teamwork Handbook", [16, 21, 22, 23, 25, 27, 28, 29, 36, 42]),
    }
    by_number = {int(item["ku_id"].split("-")[1]): item for item in NEW_UNITS}
    for filename, (title, numbers) in handbook.items():
        lines = [f"# {title}", "", "| ID | Method | Trigger | Source |", "|---|---|---|---|"]
        for number in numbers:
            item = by_number[number]
            lines.append(f"| `{item['ku_id']}` | [{item['title']}](../../sources/{item['book_id']}/cards/{item['ku_id']}.md) | {item['trigger']} | `{item['source_locator']}` |")
        (WORKFLOW / "handbook" / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_complete_sop() -> None:
    states = [
        ("problem-framing", "Problem Framing", "Establish a measurable business problem, scope boundary, and decision mandate.", ["Accountable sponsor and opportunity exist."], ["Define business problem, vision, scope, exclusions, stakeholders, subdomains, success measures, and top risks."], ["Vision and scope", "Stakeholder map", "Success measures", "Proceed/pivot/prototype decision"], ["Success measures are observable.", "Scope boundary and decision owner are explicit.", "Top risks have owners."], ["Review vision, scope, and risk assumptions."], ["Product owner", "Business sponsor", "Lead engineer"], "Return when new evidence invalidates value, scope, or domain assumptions.", "discovery-and-requirements", "handbook/management.md"),
        ("discovery-and-requirements", "Discovery and Requirements", "Create testable, owned, prioritized near-term requirements with appropriate detail.", ["Problem frame and stakeholder plan exist."], ["Elicit scenarios, rules, data, quality attributes, interfaces, exceptions, and acceptance criteria.", "Use models or prototypes to reduce uncertainty.", "Prioritize and validate the selected scope."], ["Requirements or stories", "Acceptance criteria", "Models/prototype findings", "Open issue register"], ["Near-term requirements are testable.", "Priority owner agrees on the work set.", "Key users, engineers, and testers share understanding."], ["Requirements completeness and testability review.", "Quality-attribute scenario review."], ["Business analyst", "Product owner", "Domain expert", "Engineer", "Tester"], "Return to problem framing when value or scope is unstable.", "architecture-and-domain-design", "handbook/requirements.md"),
        ("architecture-and-domain-design", "Architecture and Domain Design", "Select boundaries, invariants, integrations, and quality trade-offs that support the next value slice.", ["Testable scope slice and relevant quality attributes are known."], ["Define modules or bounded contexts, ownership, aggregate invariants, integration mappings, API/event contracts, and quality trade-offs."], ["Architecture/design decision record", "Context map or component model", "Interface contracts", "Quality trade-off notes"], ["Boundaries and ownership are reviewable.", "Quality attributes have a design response.", "Interfaces are testable."], ["Architecture and contract review.", "Aggregate invariant review where applicable."], ["Architect/lead engineer", "Domain expert", "Reviewer"], "Return to discovery when language, invariants, or quality scenarios conflict.", "plan-and-commit", "handbook/design.md"),
        ("plan-and-commit", "Plan and Commit", "Select a feasible, value-bearing work set and make scope trade-offs explicit.", ["Prioritized backlog or approved baseline exists.", "Dependencies and material risks are visible."], ["Select value slices.", "Assess capacity, risks, dependencies, and changes.", "Record commitments and deferred scope.", "Use rolling planning or formal estimation according to profile."], ["Iteration/release plan", "Risk updates", "Commitment decision", "Deferred-scope list"], ["Work set fits capacity and constraints.", "High risks have responses and triggers.", "Deferred work has an explicit rationale."], ["Capacity and risk review.", "Baseline/change authorization where required."], ["Product owner", "Project lead", "Delivery team", "Risk owner"], "Reprioritize or renegotiate scope, date, resources, or quality; never hide the trade-off.", "construct-and-integrate", "handbook/management.md"),
        ("construct-and-integrate", "Construct and Integrate", "Implement a maintainable, integrated vertical increment under configuration control.", ["The next slice has acceptance evidence and needed design decisions."], ["Implement the vertical slice.", "Run developer checks.", "Review and integrate frequently.", "Publish events safely when required.", "Maintain configuration identity."], ["Integrated build", "Code/review evidence", "Automated developer checks", "Updated configuration record"], ["Integrated build is green.", "Changes have review and test evidence.", "No unexplained contract break exists."], ["CI and regression checks.", "Configuration and contract checks."], ["Engineer", "Reviewer", "Release engineer"], "Return to design or requirements when the slice exposes an invalid assumption.", "verify-and-release", "handbook/construction.md"),
        ("verify-and-release", "Verify and Release", "Demonstrate protected behavior and decide whether the increment is safe to release.", ["Potentially shippable integrated increment exists."], ["Run acceptance, regression, and risk-driven checks.", "Validate traceability and release evidence.", "Prepare rollback and obtain release decision."], ["Test results", "Release candidate", "Traceability/release evidence", "Rollback plan", "Release decision"], ["Protected behavior passes.", "Known risk is dispositioned.", "Release has accountable approval or rejection."], ["Acceptance and regression review.", "Security, performance, recovery, and audit checks as applicable."], ["Tester", "Engineer", "Risk owner", "Release approver"], "Return to construction, design, discovery, or planning based on the defect origin.", "operate-and-learn", "handbook/testing.md"),
        ("operate-and-learn", "Operate and Learn", "Observe live outcomes and turn evidence into owned improvement decisions.", ["Release is accepted."], ["Observe demand, defects, reliability, cost, and change impact.", "Capture incidents and user feedback.", "Feed learning into value, requirements, risks, and backlog."], ["Operational observations", "Incident records", "Improvement backlog", "Updated risk/value decisions"], ["Signals reach accountable owners.", "Learning produces a follow-up decision or an explicit no-action rationale."], ["Operational review and feedback-to-backlog audit."], ["Operations", "Product owner", "Engineer", "Risk owner"], "Escalate systemic instability to planning and risk management.", "plan-and-commit", "handbook/operations.md"),
    ]
    lines = ["# SOP State Machine", "", "Each state is a control-plane contract; handbook links hold execution detail.", ""]
    for state_id, name, goal, entry, activities, outputs, exits, gates, roles, fallback, next_state, handbook in states:
        lines.extend([f"## {name}", f"- **state_id:** `{state_id}`", f"- **goal:** {goal}", f"- **entry_criteria:** {'; '.join(entry)}", f"- **activities:** {'; '.join(activities)}", f"- **outputs:** {'; '.join(outputs)}", f"- **exit_criteria:** {'; '.join(exits)}", f"- **quality_gates:** {'; '.join(gates)}", f"- **roles:** {'; '.join(roles)}", f"- **fallback:** {fallback}", f"- **next_state:** `{next_state}`", f"- **handbook:** `{handbook}`", ""])
    (WORKFLOW / "sop-state-machine.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_source_pack_reports()
    update_registry()
    update_workflow_b()
    write_complete_sop()
    print(json.dumps({"knowledge_units_added": len(NEW_UNITS), "sources_added": 3, "conflicts_added": 3}, ensure_ascii=False))


if __name__ == "__main__":
    main()
