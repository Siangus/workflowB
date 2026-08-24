"""Integrate Release It! 2e as a production-resilience source pack."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("work/se-workflow")
REGISTRY = ROOT / "registry"
SOURCES = ROOT / "sources"
WORKFLOW = ROOT / "workflow-b"
BOOK = "nygard-release-it-2e"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def source_segment(line: int) -> dict:
    return next(row for row in read_jsonl(SOURCES / BOOK / "segments.jsonl") if row["start_line"] <= line <= row["end_line"])


def unit(number: int, line: int, title: str, phase: str, kind: str, purpose: str, trigger: str, steps: list[str], checks: list[str], anti: list[str], tailoring: dict, secondary: list[str] | None = None) -> dict:
    segment = source_segment(line)
    return {
        "ku_id": f"KU-{number:04d}", "book_id": BOOK, "segment_id": segment["segment_id"], "title": title,
        "lifecycle_phase": phase, "secondary_domains": secondary or [], "knowledge_type": kind,
        "confidence": "high", "merge_status": "NEW", "needs_review": False, "status": "integrated_core",
        "purpose": purpose, "trigger": trigger, "inputs": ["System context", "Failure or change scenario"],
        "outputs": ["Resilience decision", "Testable operational evidence"], "procedure": steps,
        "checks": checks, "anti_patterns": anti, "tailoring": tailoring, "source_locator": segment["source_locator"],
    }


def card(item: dict) -> str:
    lines = [f"# {item['ku_id']}: {item['title']}", "", f"- **book_id:** `{item['book_id']}`", f"- **segment_id:** `{item['segment_id']}`", f"- **lifecycle_phase:** `{item['lifecycle_phase']}`", f"- **knowledge_type:** `{item['knowledge_type']}`", "", "## Purpose", item["purpose"], "", "## Trigger", item["trigger"], "", "## Procedure"]
    lines.extend(f"{i}. {step}" for i, step in enumerate(item["procedure"], 1))
    lines.extend(["", "## Checks"])
    lines.extend(f"- {check}" for check in item["checks"])
    lines.extend(["", "## Anti-patterns"])
    lines.extend(f"- {value}" for value in item["anti_patterns"])
    lines.extend(["", "## Tailoring", json.dumps(item["tailoring"], ensure_ascii=False), "", "## Source", f"`{item['source_locator']}`", ""])
    return "\n".join(lines)


UNITS = [
    unit(73, 1, "Production readiness and recovery mindset", "architecture", "principle", "Treat production behavior, failure recovery, and operability as design concerns rather than post-development surprises.", "A feature is functionally complete but must face real users, traffic, dependencies, and failures.", ["List expected production stresses and unknown failure modes.", "Define how the system detects, contains, and recovers from failure.", "Expose enough state for operators and developers to diagnose behavior.", "Test production-readiness scenarios before release."], ["Feature completion is separate from production readiness.", "Recovery and diagnostic behavior have owners and evidence."], ["Assuming all faults can be predicted and eliminated before release.", "Treating operations as someone else's concern."], {"light": "Production-readiness checklist for critical paths.", "heavy": "Failure model, recovery objectives, operational runbook, and resilience tests.", "cannot_remove": True}, ["risk", "release", "operations"]),
    unit(74, 491, "Stability anti-pattern detection", "architecture", "checklist", "Identify designs that amplify small faults into outages before they reach production.", "Reviewing a distributed or high-load design.", ["Map integration points and dependency chains.", "Find shared bottlenecks, blocked threads, unbounded queues/results, cascading failures, and force multipliers.", "Trace what happens when each dependency slows, fails, or returns invalid data.", "Replace or isolate the amplification path."], ["Each critical dependency has bounded time, resources, and failure behavior.", "A single failure cannot consume all shared capacity."], ["Synchronous chains without timeouts.", "Unbounded resource use.", "Many clients depending on one fragile service.", "Retries that amplify load."], {"light": "Review critical calls for timeout, bounded resources, and fallback.", "heavy": "Dependency graph, fault injection, capacity model, and resilience review.", "cannot_remove": True}, ["risk", "verification"]),
    unit(75, 255, "Stability patterns: timeouts, circuit breakers, bulkheads, and fail-fast", "architecture", "method", "Contain failures and prevent slow or broken dependencies from consuming the entire system.", "A service calls remote, slow, unreliable, or resource-constrained dependencies.", ["Set explicit timeouts for every remote or blocking operation.", "Use circuit breaking to stop calls to a failing dependency.", "Partition resources with bulkheads so one workload cannot exhaust all capacity.", "Fail fast when continuing cannot produce a valid result.", "Define fallback or degraded behavior where the business allows it."], ["Timeouts are finite and observable.", "Open/closed circuit behavior is tested.", "Resource pools and queues are bounded.", "Fallback does not claim a false success."], ["Infinite waits.", "One global thread pool for unrelated workloads.", "Returning successful-looking data after a failed dependency."], {"light": "Timeout and bounded pool for critical dependency.", "heavy": "Circuit metrics, bulkheads by workload, load shedding, and failure tests.", "cannot_remove": False}, ["construction", "verification", "operations"]),
    unit(76, 255, "Steady state, back pressure, and load shedding", "architecture", "method", "Keep demand and capacity within safe operating ranges instead of allowing overload to create collapse.", "Traffic can exceed processing capacity or downstream services can slow.", ["Define normal operating rate and safe capacity.", "Measure queue depth, latency, saturation, and rejection.", "Apply back pressure to producers or shed lower-value work.", "Use governors or admission control for expensive operations.", "Preserve critical traffic while rejecting work explicitly."], ["Overload produces controlled rejection or delay, not unbounded growth.", "Critical operations retain capacity.", "Users receive an honest status."], ["Accepting every request until all queues and threads are exhausted.", "Hiding overload behind retries."], {"light": "Bounded queue and explicit busy response.", "heavy": "Admission control, priority classes, capacity policy, and overload tests.", "cannot_remove": False}, ["requirements", "verification", "operations"]),
    unit(77, 491, "Operational transparency and control", "operations", "method", "Make running instances inspectable and controllable so failures can be diagnosed and mitigated without code changes.", "A service runs across multiple instances, hosts, containers, or environments.", ["Expose health, readiness, dependency, configuration, and version information.", "Provide structured logs, metrics, and correlation identifiers.", "Provide safe operational controls such as drain, restart, disable, or traffic shift.", "Keep control actions audited and bounded."], ["Operators can identify instance, version, configuration, and dependency state.", "Health signals distinguish ready from merely alive.", "Control actions are reversible or have a recovery path."], ["Logging without correlation or version identity.", "A health endpoint that reports alive while dependencies are unusable.", "Manual production changes with no audit."], {"light": "Versioned health/readiness endpoints and structured request IDs.", "heavy": "Full telemetry, dashboards, runbooks, audited control plane, and fault drills.", "cannot_remove": False}, ["release", "governance"]),
    unit(78, 491, "Interconnect, load balancing, and service discovery", "architecture", "method", "Design the connections between instances so traffic distribution, discovery, and failure handling remain controlled.", "A system has multiple instances, dynamic capacity, or service-to-service calls.", ["Define service identity and discovery source.", "Choose load-balancing and routing behavior.", "Handle unhealthy instances and connection limits.", "Test traffic shift, instance loss, network delay, and stale discovery."], ["Traffic does not route to known-unhealthy instances.", "Discovery failure has bounded behavior.", "Routing and capacity assumptions are documented."], ["Treating a load balancer as a complete availability solution.", "Unbounded connection creation or stale service locations."], {"light": "Health-aware load balancing and bounded client connections.", "heavy": "Failure-domain-aware routing, discovery tests, and capacity controls.", "cannot_remove": False}, ["verification", "release"]),
    unit(79, 690, "Control plane and configuration management", "release", "method", "Manage deployment, configuration, provisioning, and operational control as software with explicit ownership and visibility.", "A system spans many instances, environments, versions, or operational services.", ["Separate code, configuration, and secrets.", "Version configuration and validate it before activation.", "Automate provisioning, deployment, and rollback.", "Expose current configuration and control state.", "Test control-plane failure separately from data-plane failure."], ["A deployment can reproduce the intended version and configuration.", "Invalid configuration fails before damaging production.", "Control-plane changes are auditable."], ["Editing production configuration manually.", "Deploying code without knowing the active configuration."], {"light": "Versioned configuration and automated smoke deployment.", "heavy": "Infrastructure as code, progressive deployment, config validation, and control-plane observability.", "cannot_remove": True}, ["governance", "construction"]),
    unit(80, 690, "Security as an ongoing production process", "architecture", "principle", "Treat security, data protection, least privilege, and vulnerability response as continuous responsibilities.", "The system handles user data, privileged operations, external input, or third-party dependencies.", ["Identify sensitive data and trust boundaries.", "Apply least privilege and secure secret handling.", "Validate input and protect data integrity.", "Monitor and respond to suspicious behavior and vulnerabilities.", "Review security after changes and incidents."], ["Sensitive operations have authorization and audit evidence.", "Secrets are not embedded in code or logs.", "Vulnerability response has an owner and path."], ["Adding security checks only before launch.", "Treating successful authentication as sufficient authorization."], {"light": "Threat review and access tests for critical paths.", "heavy": "Security lifecycle, dependency scanning, incident response, and periodic review.", "cannot_remove": True}, ["requirements", "verification", "governance"]),
    unit(81, 819, "Deployment automation and continuous delivery", "release", "method", "Make deployment frequent, repeatable, observable, and reversible to reduce release risk.", "A team must release changes regularly or recover from a failed deployment.", ["Package immutable artifacts.", "Automate environment preparation and verification.", "Use staged rollout, traffic control, or canary where risk warrants.", "Separate deployment from activation when useful.", "Automate rollback or roll-forward and verify the result."], ["The same process works repeatedly across environments.", "Deployment failure stops or rolls back safely.", "Post-deployment checks verify behavior, not just process completion."], ["Large manual release windows.", "Untested rollback.", "Treating deployment completion as user-facing success."], {"light": "Automated deploy plus smoke test and rollback checklist.", "heavy": "Progressive delivery, deployment telemetry, rollback rehearsal, and release audit.", "cannot_remove": False}, ["construction", "verification"]),
    unit(82, 819, "Version and compatibility management", "release", "method", "Evolve services, interfaces, schemas, and dependencies without forcing synchronized failure across consumers.", "An API, schema, message, configuration, or dependency changes while consumers remain active.", ["Identify consumers and compatibility obligations.", "Prefer additive compatible changes.", "Version or deprecate breaking changes explicitly.", "Test old and new consumers during transition.", "Remove compatibility only after migration evidence."], ["Consumer impact is known.", "Old and new versions coexist safely during migration.", "Deprecation has a date and owner."], ["Breaking consumers without notice.", "Assuming all services deploy atomically."], {"light": "Contract tests and additive schema change.", "heavy": "Compatibility matrix, dual-read/write migration, deprecation policy, and rollout telemetry.", "cannot_remove": False}, ["architecture", "maintenance", "requirements"]),
    unit(83, 819, "Production-oriented testing and failure simulation", "verification", "method", "Validate stability and recovery behavior under realistic load, dependency failure, deployment change, and user demand.", "A system has high availability, high traffic, or costly failure consequences.", ["Define stability hypotheses and measurable success criteria.", "Test representative load and saturation.", "Inject dependency, process, network, configuration, and deployment failures in a controlled environment.", "Verify alerts, fallback, recovery, and data correctness.", "Promote proven experiments into regression checks."], ["Tests reveal failure modes before production.", "Recovery and user-visible behavior are measured.", "Experiments have a safety boundary and abort condition."], ["Testing only individual features under ideal conditions.", "Running destructive experiments without a hypothesis or rollback."], {"light": "Critical-path load and dependency-failure tests before release.", "heavy": "Staged resilience experiments, chaos program, and recurring recovery drills.", "cannot_remove": False}, ["risk", "operations"]),
    unit(84, 690, "Adaptive architecture and feedback", "maintenance", "principle", "Evolve people, process, architecture, and information flow together as demand, scale, and failure evidence change.", "The system or its environment changes faster than initial assumptions remain valid.", ["Observe demand, incidents, capacity, and change cost.", "Identify which architectural or process assumption is now limiting.", "Make a small reversible improvement.", "Measure the result and feed it into the next decision."], ["Adaptation is driven by evidence.", "Architecture and operational changes have owners and follow-up measures."], ["Adding a large framework before proving the constraint.", "Optimizing one layer while ignoring the system."], {"light": "Retrospective action tied to one measurable pain.", "heavy": "Architecture evolution roadmap and organizational feedback loops.", "cannot_remove": False}, ["feedback", "planning"]),
    unit(85, 819, "Chaos engineering as hypothesis-driven validation", "verification", "method", "Discover systemic weaknesses by deliberately introducing controlled failures and checking whether steady-state expectations hold.", "The system has established observability, safe abort controls, and a resilience hypothesis worth testing.", ["Define steady-state behavior and user-impact measure.", "Form a failure hypothesis.", "Run the smallest safe experiment in an appropriate environment.", "Observe impact, stop if safety limits are crossed, and analyze results.", "Fix the weakness and repeat the experiment."], ["Steady state is measurable before the experiment.", "Blast radius and abort conditions are explicit.", "Findings create remediation and regression evidence."], ["Treating chaos as random destruction.", "Running experiments before basic monitoring and recovery exist."], {"light": "Staged dependency-failure experiment in preproduction.", "heavy": "Production-safe chaos program with governance, blast-radius controls, and recurring experiments.", "cannot_remove": False}, ["risk", "operations"]),
]


def main() -> None:
    cards_dir = SOURCES / BOOK / "cards"
    cards_dir.mkdir(exist_ok=True)
    for item in UNITS:
        (cards_dir / f"{item['ku_id']}.md").write_text(card(item), encoding="utf-8")
    segments = read_jsonl(SOURCES / BOOK / "segments.jsonl")
    used = {item["segment_id"] for item in UNITS}
    report = ["# Integration Report", "", f"- **book_id:** `{BOOK}`", "- **chapters read:** 17", f"- **knowledge units:** {len(UNITS)}", "- **status:** `integrated_core`", "", "## Pending enrichment segments", ""]
    report.extend(f"- `{row['segment_id']}`" for row in segments if row["segment_id"] not in used)
    (SOURCES / BOOK / "integration-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (SOURCES / BOOK / "book-summary.md").write_text("""# Book Summary: Release It!, Second Edition\n\nThe book moves from feature-complete software to production-ready systems. It uses failure case studies to show that small faults become outages through dependency chains, resource exhaustion, overload, and poor operational visibility. It then develops stability principles and patterns: timeouts, circuit breakers, bulkheads, fail-fast behavior, bounded resources, back pressure, load shedding, governors, transparency, and control. Later chapters cover foundations, interconnect, control planes, security, deployment automation, version compatibility, organizational adaptation, and chaos engineering.\n\nIts durable contribution to Workflow B is a recovery-oriented design discipline: define steady state, assume faults, bound blast radius, make runtime state visible, automate deployment and rollback, preserve compatibility, and validate resilience with realistic load and controlled failure experiments.\n""", encoding="utf-8")

    sources = read_jsonl(REGISTRY / "sources.jsonl")
    if BOOK not in {row["book_id"] for row in sources}:
        inv = json.loads((SOURCES / BOOK / "inventory.json").read_text(encoding="utf-8"))
        sources.append({"book_id": BOOK, "title": "Release It!, Second Edition", "type": "production-resilience-and-stability", "status": "integrated_core", "files": [row["path"] for row in inv["files"]], "segments": inv["segment_count"], "chapters_read": 17, "knowledge_units": len(UNITS), "confidence": "high"})
    write_jsonl(REGISTRY / "sources.jsonl", sources)

    segments_registry = read_jsonl(REGISTRY / "segments.jsonl")
    known = {row["segment_id"] for row in segments_registry}
    segments_registry.extend(row for row in segments if row["segment_id"] not in known)
    write_jsonl(REGISTRY / "segments.jsonl", segments_registry)

    units_registry = read_jsonl(REGISTRY / "knowledge-units.jsonl")
    known_units = {row["ku_id"] for row in units_registry}
    units_registry.extend(item for item in UNITS if item["ku_id"] not in known_units)
    write_jsonl(REGISTRY / "knowledge-units.jsonl", units_registry)

    conflicts = read_jsonl(REGISTRY / "conflicts.jsonl")
    if "CF-0007" not in {row["conflict_id"] for row in conflicts}:
        conflicts.extend([
            {"conflict_id": "CF-0007", "topic": "Feature complete versus production ready", "left": {"ku_ids": ["KU-0024"], "claim": "A completed increment is integrated and verified."}, "right": {"ku_ids": ["KU-0073"], "claim": "Production readiness also requires recovery, transparency, control, and resilience evidence."}, "context_difference": "Development acceptance versus production-critical delivery.", "workflow_impact": "high", "resolution_status": "combined"},
            {"conflict_id": "CF-0008", "topic": "Deployment cadence", "left": {"ku_ids": ["KU-0025"], "claim": "Keep increments potentially shippable and deliver frequently."}, "right": {"ku_ids": ["KU-0081"], "claim": "Deployment must be automated, staged, observable, and reversible."}, "context_difference": "Feature delivery practice versus production rollout safety.", "workflow_impact": "medium", "resolution_status": "combined"},
        ])
    write_jsonl(REGISTRY / "conflicts.jsonl", conflicts)

    domains = json.loads((REGISTRY / "lifecycle-spine.json").read_text(encoding="utf-8"))["domains"]
    primary = Counter(item["lifecycle_phase"] for item in units_registry)
    secondary = Counter(domain for item in units_registry for domain in item["secondary_domains"])
    lines = ["# Coverage", "", "| Domain | Primary | Secondary | Class | Next action |", "|---|---:|---:|---|---|"]
    for domain in domains:
        total = primary[domain] + secondary[domain]
        cls = "strong" if primary[domain] >= 3 and total >= 5 else "usable" if total >= 3 else "stub" if total else "none"
        lines.append(f"| `{domain}` | {primary[domain]} | {secondary[domain]} | `{cls}` | Use and refine with project evidence |")
    (REGISTRY / "coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    log = (REGISTRY / "merge-log.md").read_text(encoding="utf-8")
    if "MERGE-0004" not in log:
        log += f"\n## MERGE-0004\n\n- **at:** {datetime.now(timezone.utc).isoformat()}\n- **source:** `{BOOK}`\n- **action:** production resilience deep-read and fold-in\n- **chapters read:** 17\n- **knowledge units added:** {len(UNITS)}\n- **conflicts recorded:** 2\n- **status:** draft-ready; reliability, deployment, and failure testing strengthened\n"
        (REGISTRY / "merge-log.md").write_text(log, encoding="utf-8")

    design = WORKFLOW / "handbook" / "design.md"
    design_text = design.read_text(encoding="utf-8")
    if "Release It!" not in design_text:
        design.write_text(design_text.rstrip() + "\n\n## Production Resilience\n\n| ID | Method | Trigger | Source |\n|---|---|---|---|\n" + "\n".join(f"| `{item['ku_id']}` | [{item['title']}](../../sources/{BOOK}/cards/{item['ku_id']}.md) | {item['trigger']} | `{item['source_locator']}` |" for item in UNITS if item["lifecycle_phase"] == "architecture") + "\n", encoding="utf-8")

    testing = WORKFLOW / "handbook" / "testing.md"
    testing_text = testing.read_text(encoding="utf-8")
    if "Stability and failure testing" not in testing_text:
        testing.write_text(testing_text.rstrip() + "\n\n## Stability and failure testing\n\n| ID | Method | Trigger | Source |\n|---|---|---|---|\n" + "\n".join(f"| `{item['ku_id']}` | [{item['title']}](../../sources/{BOOK}/cards/{item['ku_id']}.md) | {item['trigger']} | `{item['source_locator']}` |" for item in UNITS if item["lifecycle_phase"] == "verification") + "\n", encoding="utf-8")

    ops = WORKFLOW / "handbook" / "operations.md"
    ops_text = ops.read_text(encoding="utf-8") if ops.exists() else "# Operations Handbook\n"
    if "Release It!" not in ops_text:
        ops.write_text(ops_text.rstrip() + "\n\n## Production resilience\n\n| ID | Method | Trigger | Source |\n|---|---|---|---|\n" + "\n".join(f"| `{item['ku_id']}` | [{item['title']}](../../sources/{BOOK}/cards/{item['ku_id']}.md) | {item['trigger']} | `{item['source_locator']}` |" for item in UNITS if item["lifecycle_phase"] in {"operations", "release", "maintenance"}) + "\n", encoding="utf-8")

    sop = WORKFLOW / "sop-state-machine.md"
    sop_text = sop.read_text(encoding="utf-8")
    marker = "- **activities:** Run acceptance, regression, and risk-driven checks.; Validate traceability and release evidence.; Prepare rollback and obtain release decision."
    replacement = "- **activities:** Run acceptance, regression, load, security, recovery, and failure-mode checks as applicable.; Validate traceability and release evidence.; Verify deployment artifact, configuration, health signals, and rollback.; Obtain release decision."
    if marker in sop_text:
        sop.write_text(sop_text.replace(marker, replacement).replace("- **quality_gates:** Acceptance and regression review.; Security, performance, recovery, and audit checks as applicable.", "- **quality_gates:** Acceptance and regression review.; Stability and failure-mode review.; Security, performance, recovery, and audit checks as applicable.; Deployment/rollback readiness check."), encoding="utf-8")

    print(json.dumps({"book": BOOK, "chapters_read": 17, "knowledge_units_added": len(UNITS), "conflicts_added": 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
