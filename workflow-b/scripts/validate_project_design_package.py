"""Validate Workflow B's minimum project design-readiness evidence."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_DOCUMENTS = (
    "00-charter.md",
    "01-requirements-baseline.md",
    "02-domain-and-state-model.md",
    "03-quality-attribute-scenarios.md",
    "04-architecture-overview.md",
    "05-runtime-and-integration-flows.md",
    "06-data-consistency-and-recovery.md",
    "07-api-and-interface-contracts.md",
    "09-risk-and-security-review.md",
    "10-test-and-acceptance-strategy.md",
    "11-traceability-matrix.md",
    "12-v1-plan.md",
    "13-design-readiness-review.md",
    "arc42.md",
)
ARC42_SECTIONS = (
    "## 1. Introduction and Goals",
    "## 2. Architecture Constraints",
    "## 3. System Scope and Context",
    "## 4. Solution Strategy",
    "## 5. Building Block View",
    "## 6. Runtime View",
    "## 7. Deployment View",
    "## 8. Cross-Cutting Concepts",
    "## 9. Architecture Decisions",
    "## 10. Quality Requirements",
    "## 11. Risks and Technical Debt",
    "## 12. Glossary",
)
REQUIREMENT_PATTERN = re.compile(r"^\|\s*(FR-[A-Z]+-\d+)\s*\|")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_ids(path: Path) -> dict[str, str]:
    return {
        match.group(1): line
        for line in read_text(path).splitlines()
        if (match := REQUIREMENT_PATTERN.match(line))
    }


def validate(design_path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    for filename in REQUIRED_DOCUMENTS:
        if not (design_path / filename).is_file():
            errors.append(f"missing required design artifact: {filename}")

    adr_dir = design_path / "08-adr"
    adr_files = sorted(adr_dir.glob("ADR-*.md")) if adr_dir.is_dir() else []
    if not adr_files:
        errors.append("missing ADR evidence: expected 08-adr/ADR-*.md")

    arc42_path = design_path / "arc42.md"
    if arc42_path.is_file():
        arc42_text = read_text(arc42_path)
        for section in ARC42_SECTIONS:
            if section not in arc42_text:
                errors.append(f"arc42 missing section: {section}")

    requirements_path = design_path / "01-requirements-baseline.md"
    traceability_path = design_path / "11-traceability-matrix.md"
    requirement_ids: dict[str, str] = {}
    trace_rows: dict[str, str] = {}
    if requirements_path.is_file():
        requirement_ids = markdown_ids(requirements_path)
        if not requirement_ids:
            errors.append("requirements baseline contains no FR-* rows")
    if traceability_path.is_file():
        trace_rows = markdown_ids(traceability_path)
        if not trace_rows:
            errors.append("traceability matrix contains no FR-* rows")

    for requirement_id in requirement_ids:
        trace_row = trace_rows.get(requirement_id)
        if trace_row is None:
            errors.append(f"requirement lacks a traceability row: {requirement_id}")
            continue
        columns = [column.strip() for column in trace_row.strip("|").split("|")]
        if len(columns) < 6 or not columns[4] or columns[4] in {"N/A", "TBD"}:
            errors.append(f"requirement lacks a test identifier: {requirement_id}")

    review_path = design_path / "13-design-readiness-review.md"
    if review_path.is_file():
        review_text = read_text(review_path)
        approved = re.search(r"^- \[x\] (APPROVED|APPROVED_WITH_RISKS)$", review_text, re.MULTILINE)
        if not approved:
            errors.append("design-readiness review lacks APPROVED or APPROVED_WITH_RISKS decision")
        if "- [x] REWORK_REQUIRED" in review_text:
            errors.append("design-readiness review marks REWORK_REQUIRED")

    stats = {
        "required_documents": len(REQUIRED_DOCUMENTS),
        "requirements": len(requirement_ids),
        "trace_rows": len(trace_rows),
        "adr_files": len(adr_files),
    }
    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design_package", type=Path, help="path to the project docs/design directory")
    args = parser.parse_args()
    design_path = args.design_package.resolve()
    errors, warnings, stats = validate(design_path)
    result = {
        "status": "blocked" if errors else ("warnings" if warnings else "ready"),
        "design_package": str(design_path),
        "stats": stats,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
