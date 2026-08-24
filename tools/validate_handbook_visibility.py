"""Validate the progressive-disclosure Workflow B handbook."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "workflow-b"
REGISTRY = ROOT / "registry"
STATES = ["problem-framing", "requirements", "architecture", "design-readiness", "construction", "verification", "release", "operations"]
CROSS_CUTTING = ["security", "reliability", "performance", "consistency", "observability", "data-and-privacy"]


def read_knowledge_ids() -> set[str]:
    return {json.loads(line)["ku_id"] for line in (REGISTRY / "knowledge-units.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()}


def validate() -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = WORKFLOW / "manifest.yaml"
    if not manifest.exists():
        errors.append("workflow-b/manifest.yaml is missing")
    else:
        manifest_text = manifest.read_text(encoding="utf-8")
        for required in ["L0/router.md", "L0/principles.md", "L0/project-profiles.md", "L0/sop-state-machine.md"]:
            if required not in manifest_text:
                errors.append(f"manifest missing default route: {required}")
        paths = re.findall(r"^\s+- (\S+\.md)$", manifest_text, re.MULTILINE)
        for relative in paths:
            if not (WORKFLOW / relative).exists():
                errors.append(f"manifest path missing: {relative}")

    for relative in ["L0/router.md", "L0/principles.md", "L0/project-profiles.md", "L0/sop-state-machine.md", "L3/provenance-guide.md"]:
        if not (WORKFLOW / relative).exists():
            errors.append(f"required visibility file missing: {relative}")

    full_sop = (WORKFLOW / "sop-state-machine.md")
    if not full_sop.exists():
        errors.append("compatibility SOP is missing")
    else:
        full_sop_text = full_sop.read_text(encoding="utf-8")
        if "## Design Readiness" not in full_sop_text:
            errors.append("compatibility SOP bypasses design-readiness")
        if "accepted by an accountable human" not in full_sop_text:
            errors.append("construction entry does not require accountable human acceptance")

    design_package = WORKFLOW / "templates" / "project-design-package"
    required_design_docs = [
        "00-charter.md", "01-requirements-baseline.md", "evidence-register.md", "02-domain-and-state-model.md",
        "03-quality-attribute-scenarios.md", "04-architecture-overview.md", "arc42.md", "05-runtime-and-integration-flows.md",
        "06-data-consistency-and-recovery.md", "07-api-and-interface-contracts.md", "09-risk-and-security-review.md",
        "10-test-and-acceptance-strategy.md", "11-traceability-matrix.md", "12-v1-plan.md", "13-design-readiness-review.md",
    ]
    for filename in required_design_docs:
        if not (design_package / filename).exists():
            errors.append(f"project design package missing: {filename}")
    if not (design_package / "08-adr" / "README.md").exists():
        errors.append("project design package missing: 08-adr/README.md")

    for state in STATES:
        directory = WORKFLOW / "states" / state
        for filename in ["playbook.md", "checklist.md", "methods-index.md"]:
            if not (directory / filename).exists():
                errors.append(f"state {state} missing {filename}")

    for module in CROSS_CUTTING:
        if not (WORKFLOW / "cross-cutting" / module / "index.md").exists():
            errors.append(f"cross-cutting module missing: {module}")

    knowledge_ids = read_knowledge_ids()
    method_ids: set[str] = set()
    for path in (WORKFLOW / "L2" / "methods").glob("KU-*.md"):
        method_ids.add(path.stem)
        if path.stem not in knowledge_ids:
            errors.append(f"L2 method has no registry knowledge unit: {path.stem}")

    for path in list((WORKFLOW / "states").glob("*/methods-index.md")) + list((WORKFLOW / "cross-cutting").glob("*/index.md")):
        text = path.read_text(encoding="utf-8")
        for ku_id in re.findall(r"`(KU-\d+)`", text):
            if ku_id not in knowledge_ids:
                errors.append(f"{path.relative_to(WORKFLOW)} references unknown knowledge unit: {ku_id}")
            if not (WORKFLOW / "L2" / "methods" / f"{ku_id}.md").exists():
                errors.append(f"{path.relative_to(WORKFLOW)} references missing L2 method: {ku_id}")

    link_errors: list[str] = []
    for source in WORKFLOW.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (source.parent / target).resolve()
            if not resolved.exists():
                link_errors.append(f"{source.relative_to(WORKFLOW)} -> {target}")
    errors.extend(f"broken relative link: {entry}" for entry in link_errors)

    if not method_ids:
        errors.append("no L2 methods generated")
    if len(method_ids) < len(knowledge_ids):
        warnings.append(f"L2 contains {len(method_ids)} methods for {len(knowledge_ids)} registry units; legacy/seed units may remain provenance-only")

    stats = {"states": len(STATES), "cross_cutting_modules": len(CROSS_CUTTING), "l2_methods": len(method_ids), "registry_units": len(knowledge_ids), "broken_links": len(link_errors)}
    return errors, warnings, stats


def main() -> int:
    errors, warnings, stats = validate()
    result = {"status": "blocked" if errors else ("warnings" if warnings else "ready"), "stats": stats, "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
