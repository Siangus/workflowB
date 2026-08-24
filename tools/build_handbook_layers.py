"""Generate progressive-disclosure Workflow B handbook layers."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("work/se-workflow")
WF = ROOT / "workflow-b"
REGISTRY = ROOT / "registry"


STATES = {
    "problem-framing": {
        "title": "Problem Framing",
        "goal": "Establish the problem, scope, stakeholders, success evidence, and decision mandate.",
        "entry": "An opportunity, pain, regulation, or strategic initiative has an accountable sponsor.",
        "activities": ["Define the business problem and product vision.", "Set scope, exclusions, constraints, and success measures.", "Identify stakeholder and user classes.", "Classify major subdomains and top risks."],
        "outputs": ["Vision and scope", "Stakeholder map", "Success measures", "Initial risk list", "Proceed/pivot/prototype decision"],
        "exit": ["Problem and value are observable.", "Scope boundary and decision owner are explicit.", "Top risks have owners and triggers."],
        "gates": ["Vision and scope review", "Stakeholder coverage review", "Risk assumption review"],
        "fallback": "Return here when new evidence invalidates value, scope, or domain assumptions.",
        "next": "requirements",
        "cross": ["security", "data-and-privacy", "reliability"],
        "methods": ["KU-0009", "KU-0016", "KU-0028", "KU-0029", "KU-0042", "KU-0073"],
    },
    "requirements": {
        "title": "Discovery and Requirements",
        "goal": "Create owned, prioritized, testable near-term requirements with appropriate detail.",
        "entry": "A problem frame and stakeholder plan exist.",
        "activities": ["Elicit scenarios, rules, data, quality attributes, interfaces, and exceptions.", "Use models or prototypes to reduce uncertainty.", "Prioritize and validate the selected scope.", "Choose baseline or just-in-time elaboration according to profile."],
        "outputs": ["Requirements or stories", "Acceptance criteria", "Business-rule catalog", "Models/prototype findings", "Open issue register"],
        "exit": ["Near-term requirements are testable.", "Priority owner agrees on the work set.", "Key users, engineers, and testers share understanding.", "Quality attributes have measurable scenarios."],
        "gates": ["Completeness and testability review", "Quality-attribute scenario review", "Stakeholder confirmation"],
        "fallback": "Return to problem framing when value or scope is unstable; create a prototype or spike for unresolved uncertainty.",
        "next": "architecture",
        "cross": ["security", "data-and-privacy", "performance", "consistency", "reliability"],
        "methods": ["KU-0030", "KU-0031", "KU-0032", "KU-0033", "KU-0034", "KU-0035", "KU-0036", "KU-0037", "KU-0038", "KU-0039", "KU-0040", "KU-0041", "KU-0051", "KU-0076"],
    },
    "architecture": {
        "title": "Architecture and Domain Design",
        "goal": "Select boundaries, quality tactics, integration contracts, and implementation patterns for the next value slice.",
        "entry": "Testable scope and architecturally significant requirements are known.",
        "activities": ["Define quality attribute scenarios.", "Choose module, runtime, deployment, and behavior views.", "Apply incremental architecture design.", "Select domain, data, concurrency, presentation, and distribution patterns only when justified.", "Document interfaces, rationale, mappings, and debt.", "Evaluate the architecture against stakeholder risks."],
        "outputs": ["Quality attribute scenarios", "Architecture decision record", "Selected views and mappings", "Interface/behavior contracts", "Pattern decision", "Evaluation findings", "Architecture debt items"],
        "exit": ["Architecture drivers have design responses.", "Boundaries and ownership are reviewable.", "Interfaces and behavior are testable.", "Major trade-offs and risks are recorded.", "Documentation is usable by intended stakeholders."],
        "gates": ["Quality scenario review", "Architecture and contract review", "View/documentation completeness review", "Concurrency/invariant review", "Architecture risk evaluation"],
        "fallback": "Return to requirements when quality scenarios or language conflict; create a spike when architecture risk is not understood.",
        "next": "construction",
        "cross": ["security", "data-and-privacy", "performance", "consistency", "reliability", "observability"],
        "methods": ["KU-0015", "KU-0017", "KU-0018", "KU-0019", "KU-0020", "KU-0043", "KU-0044", "KU-0045", "KU-0047", "KU-0048", "KU-0049", "KU-0050", "KU-0051", "KU-0052", "KU-0053", "KU-0054", "KU-0055", "KU-0056", "KU-0057", "KU-0058", "KU-0059", "KU-0060", "KU-0062", "KU-0063", "KU-0064", "KU-0065", "KU-0068", "KU-0071", "KU-0075", "KU-0078"],
    },
    "construction": {
        "title": "Construct and Integrate",
        "goal": "Implement a maintainable, tested, integrated vertical increment under configuration control.",
        "entry": "The next slice has acceptance evidence and required design decisions.",
        "activities": ["Implement the smallest vertical slice.", "Run developer checks and focused integration tests.", "Review and integrate frequently.", "Apply transactions, idempotency, timeouts, and boundaries from the architecture.", "Update configuration and interface identity."],
        "outputs": ["Integrated build", "Code/review evidence", "Automated developer checks", "Updated configuration record", "Updated traceability"],
        "exit": ["Integrated build is green.", "Changes have review and test evidence.", "No unexplained contract break exists.", "The slice is demonstrable and potentially releasable."],
        "gates": ["CI and regression checks", "Code/design review", "Configuration and contract checks"],
        "fallback": "Return to architecture or requirements when the slice exposes an invalid assumption; record new debt rather than hiding it.",
        "next": "verification",
        "cross": ["security", "performance", "consistency", "reliability", "observability"],
        "methods": ["KU-0020", "KU-0024", "KU-0025", "KU-0026", "KU-0063", "KU-0065", "KU-0066", "KU-0074", "KU-0075", "KU-0076", "KU-0079"],
    },
    "verification": {
        "title": "Verify and Accept",
        "goal": "Demonstrate intended behavior, quality attributes, failure behavior, and acceptance evidence.",
        "entry": "A potentially shippable integrated increment exists.",
        "activities": ["Run unit, integration, contract, acceptance, and regression checks.", "Run performance, security, recovery, and failure-mode tests as applicable.", "Validate traceability and release evidence.", "Disposition known failures and risks."],
        "outputs": ["Test results", "Acceptance decision", "Coverage/traceability evidence", "Failure findings", "Release recommendation"],
        "exit": ["Protected behavior passes.", "Quality targets have evidence.", "Known risks have disposition.", "Acceptance owner approves or rejects explicitly."],
        "gates": ["Acceptance and regression review", "Quality-attribute review", "Stability/failure review", "Security review where enabled"],
        "fallback": "Return to construction, architecture, requirements, or planning based on defect origin.",
        "next": "release",
        "cross": ["security", "performance", "consistency", "reliability", "observability"],
        "methods": ["KU-0013", "KU-0014", "KU-0026", "KU-0032", "KU-0034", "KU-0037", "KU-0041", "KU-0050", "KU-0053", "KU-0074", "KU-0083", "KU-0085"],
    },
    "release": {
        "title": "Release Readiness",
        "goal": "Make a verified increment deployable, compatible, recoverable, and auditable.",
        "entry": "Verification exit criteria are met.",
        "activities": ["Verify artifact, configuration, schema, and interface identity.", "Run deployment and smoke checks.", "Validate migration compatibility and rollback/roll-forward.", "Obtain the accountable release decision."],
        "outputs": ["Release candidate", "Approval record", "Deployment evidence", "Rollback plan", "Compatibility record"],
        "exit": ["Build and configuration identity are verified.", "Monitoring and recovery are ready.", "Approval is complete.", "Known compatibility risks are accepted or resolved."],
        "gates": ["Release checklist", "Deployment/rollback check", "Compatibility check", "Security/audit check"],
        "fallback": "Return to verification or construction when release evidence fails; use rollback or roll-forward according to the compatibility plan.",
        "next": "operations",
        "cross": ["security", "reliability", "observability", "data-and-privacy", "consistency"],
        "methods": ["KU-0040", "KU-0041", "KU-0046", "KU-0079", "KU-0081", "KU-0082"],
    },
    "operations": {
        "title": "Operate and Learn",
        "goal": "Observe live outcomes, control failure impact, and feed evidence back into engineering decisions.",
        "entry": "Release is accepted and operational ownership exists.",
        "activities": ["Observe demand, defects, reliability, cost, and change impact.", "Capture incidents and user feedback.", "Use bounded controls, recovery, and safe operational actions.", "Feed evidence into requirements, risks, architecture debt, and planning."],
        "outputs": ["Operational observations", "Incident records", "Improvement backlog", "Updated risk/value decisions"],
        "exit": ["Signals reach accountable owners.", "Recovery behavior is tested or rehearsed.", "Learning produces an owned follow-up decision."],
        "gates": ["Operational review", "Feedback-to-backlog audit", "Recovery evidence review"],
        "fallback": "Escalate systemic instability to planning and risk management.",
        "next": "plan-and-commit",
        "cross": ["reliability", "observability", "security", "performance"],
        "methods": ["KU-0073", "KU-0075", "KU-0077", "KU-0078", "KU-0080", "KU-0084", "KU-0085"],
    },
}


def write_state_files() -> None:
    registry_units = {item["ku_id"]: item for item in json.loads("[" + ",".join((ROOT / "registry/knowledge-units.jsonl").read_text(encoding="utf-8").splitlines()) + "]")}
    for state_id, data in STATES.items():
        directory = WF / "states" / state_id
        directory.mkdir(parents=True, exist_ok=True)
        playbook = [f"# {data['title']} Playbook", "", f"**Goal:** {data['goal']}", "", f"**Entry:** {data['entry']}", "", "## Activities"]
        playbook.extend(f"{i}. {value}" for i, value in enumerate(data["activities"], 1))
        playbook.extend(["", "## Outputs"])
        playbook.extend(f"- {value}" for value in data["outputs"])
        playbook.extend(["", "## Exit Evidence"])
        playbook.extend(f"- {value}" for value in data["exit"])
        playbook.extend(["", "## Quality Gates"])
        playbook.extend(f"- {value}" for value in data["gates"])
        playbook.extend(["", f"**Fallback:** {data['fallback']}", f"**Next state:** `{data['next']}`", "", "## Load Next", f"- `states/{state_id}/checklist.md`", f"- `states/{state_id}/methods-index.md`"])
        playbook.extend(f"- `cross-cutting/{value}/index.md`" for value in data["cross"])
        (directory / "playbook.md").write_text("\n".join(playbook) + "\n", encoding="utf-8")

        checklist = [f"# {data['title']} Checklist", "", "Check each item with evidence; do not use percentage-complete as a substitute.", ""]
        checklist.extend(f"- [ ] {value}" for value in data["exit"])
        checklist.extend(["", "## Gates"])
        checklist.extend(f"- [ ] {value}" for value in data["gates"])
        (directory / "checklist.md").write_text("\n".join(checklist) + "\n", encoding="utf-8")

        index = [f"# {data['title']} Methods Index", "", "Load only the method needed for the current activity.", "", "| ID | Method | Trigger | Source |", "|---|---|---|---|"]
        for ku_id in data["methods"]:
            item = registry_units.get(ku_id)
            if not item:
                continue
            index.append(f"| `{ku_id}` | [{item['title']}](../../L2/methods/{ku_id}.md) | {item['trigger']} | `{item['source_locator']}` |")
        (directory / "methods-index.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def write_cross_cutting() -> None:
    modules = {
        "security": ("Security", ["problem-framing", "requirements", "architecture", "construction", "verification", "release", "operations"], ["KU-0049", "KU-0080"]),
        "reliability": ("Reliability", ["problem-framing", "requirements", "architecture", "construction", "verification", "release", "operations"], ["KU-0045", "KU-0073", "KU-0075", "KU-0076", "KU-0077", "KU-0078", "KU-0083", "KU-0085"]),
        "performance": ("Performance and Capacity", ["requirements", "architecture", "construction", "verification", "release", "operations"], ["KU-0048", "KU-0076", "KU-0078", "KU-0083"]),
        "consistency": ("Consistency and Idempotency", ["requirements", "architecture", "construction", "verification", "release"], ["KU-0019", "KU-0020", "KU-0067", "KU-0075", "KU-0076"]),
        "observability": ("Observability and Control", ["requirements", "architecture", "construction", "verification", "release", "operations"], ["KU-0054", "KU-0077", "KU-0079", "KU-0083"]),
        "data-and-privacy": ("Data and Privacy", ["problem-framing", "requirements", "architecture", "construction", "verification", "release"], ["KU-0034", "KU-0041", "KU-0049", "KU-0080", "KU-0082"]),
    }
    all_units = {item["ku_id"]: item for item in json.loads("[" + ",".join((ROOT / "registry/knowledge-units.jsonl").read_text(encoding="utf-8").splitlines()) + "]")}
    for slug, (title, states, methods) in modules.items():
        directory = WF / "cross-cutting" / slug
        directory.mkdir(parents=True, exist_ok=True)
        lines = [f"# {title}", "", "Enable this module only when the project profile or current risk triggers it.", "", "| State | Question |", "|---|---|"]
        questions = {"problem-framing": "What assets, failure costs, obligations, or targets matter?", "requirements": "What must the system guarantee and how will it be measured?", "architecture": "Which boundaries, tactics, contracts, or patterns provide it?", "construction": "Which implementation controls must exist?", "verification": "What test or review evidence proves it?", "release": "What must be checked before exposure?", "operations": "What must be observed, controlled, and recovered?"}
        lines.extend(f"| `{state}` | {questions[state]} |" for state in states)
        lines.extend(["", "## Methods"])
        for ku_id in methods:
            item = all_units.get(ku_id)
            if item:
                lines.append(f"- `{ku_id}` [{item['title']}](../../L2/methods/{ku_id}.md) - {item['trigger']}")
        (directory / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_l2() -> None:
    methods_dir = WF / "L2" / "methods"
    patterns_dir = WF / "L2" / "patterns"
    tests_dir = WF / "L2" / "test-strategies"
    for directory in [methods_dir, patterns_dir, tests_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    units = json.loads("[" + ",".join((ROOT / "registry/knowledge-units.jsonl").read_text(encoding="utf-8").splitlines()) + "]")
    for item in units:
        path = methods_dir / f"{item['ku_id']}.md"
        if path.exists():
            continue
        lines = [f"# {item['ku_id']}: {item['title']}", "", f"**Type:** `{item['knowledge_type']}`", f"**Lifecycle:** `{item['lifecycle_phase']}`", f"**Trigger:** {item['trigger']}", "", "## Purpose", item["purpose"], "", "## Procedure"]
        lines.extend(f"{i}. {step}" for i, step in enumerate(item["procedure"], 1))
        lines.extend(["", "## Checks"])
        lines.extend(f"- {check}" for check in item["checks"])
        lines.extend(["", "## Tailoring", json.dumps(item["tailoring"], ensure_ascii=False), "", "## Provenance", f"- Knowledge unit: `{item['ku_id']}`", f"- Source: `{item['source_locator']}`", ""])
        path.write_text("\n".join(lines), encoding="utf-8")
    (methods_dir / "README.md").write_text("# L2 Methods\n\nLoad individual method files only for the current activity. Each file preserves its knowledge-unit ID and source locator.\n", encoding="utf-8")
    (patterns_dir / "README.md").write_text("# L2 Patterns\n\nUse pattern entries after a concrete design problem is identified. Do not select a pattern by name alone; record the problem, alternatives, and trade-offs.\n\nPattern knowledge is currently indexed through the method files for DDD and enterprise application architecture.\n", encoding="utf-8")
    (tests_dir / "README.md").write_text("# L2 Test Strategies\n\nLoad this directory when selecting unit, integration, contract, acceptance, performance, recovery, or failure-injection tests.\n", encoding="utf-8")


def write_l3() -> None:
    directory = WF / "L3"
    directory.mkdir(exist_ok=True)
    (directory / "provenance-guide.md").write_text("""# L3 Provenance Guide

L3 is loaded only for traceability, disagreement, audit, or deep study.

```text
L1/L2 method
→ knowledge-unit ID
→ registry/knowledge-units.jsonl
→ sources/<book-id>/cards/<KU-ID>.md
→ source locator in the original book segment
```

Use `registry/conflicts.jsonl` when two methods are context-dependent or materially disagree. Use `registry/merge-log.md` to understand when a source entered B. Do not load all source cards during ordinary state execution.
""", encoding="utf-8")


if __name__ == "__main__":
    write_state_files()
    write_cross_cutting()
    write_l2()
    write_l3()
    print("handbook layers generated")
