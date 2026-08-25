"""Validate Workflow B's minimum project design-readiness evidence."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_DOCUMENTS = (
    "00-charter.md",
    "00-document-set-index.md",
    "01-requirements-baseline.md",
    "software-requirements-specification.md",
    "product-requirements-specification.md",
    "technical-design.md",
    "verification-and-acceptance-plan.md",
    "operations-and-slo.md",
    "evidence-register.md",
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
ARC42_SECTION_OPTIONS = (
    ("## 1. Introduction and Goals", "## 1. 引言与目标"),
    ("## 2. Architecture Constraints", "## 2. 架构约束"),
    ("## 3. System Scope and Context", "## 3. 系统范围与上下文"),
    ("## 4. Solution Strategy", "## 4. 解决方案策略"),
    ("## 5. Building Block View", "## 5. 构建块视图"),
    ("## 6. Runtime View", "## 6. 运行时视图"),
    ("## 7. Deployment View", "## 7. 部署视图"),
    ("## 8. Cross-Cutting Concepts", "## 8. 横切概念"),
    ("## 9. Architecture Decisions", "## 9. 架构决策"),
    ("## 10. Quality Requirements", "## 10. 质量需求"),
    ("## 11. Risks and Technical Debt", "## 11. 风险与技术债"),
    ("## 12. Glossary", "## 12. 词汇表"),
)
REQUIREMENT_PATTERN = re.compile(r"^\|\s*(FR-(?:[A-Z]+-)?\d+)\s*\|")
SCENARIO_ID_PATTERN = re.compile(r"^\|\s*([A-Z][A-Z0-9-]*-\d+)\s*\|")
SCENARIO_REFERENCE_PATTERN = re.compile(r"[A-Z][A-Z0-9-]*-\d+")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_ids(path: Path) -> dict[str, str]:
    return {
        match.group(1): line
        for line in read_text(path).splitlines()
        if (match := REQUIREMENT_PATTERN.match(line))
    }


def scenario_ids(path: Path) -> set[str]:
    return {
        match.group(1)
        for line in read_text(path).splitlines()
        if (match := SCENARIO_ID_PATTERN.match(line))
    }


def validate(design_path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    for filename in REQUIRED_DOCUMENTS:
        if not (design_path / filename).is_file():
            errors.append(f"missing required design artifact: {filename}")

    primary_documents = {
        "product-requirements-specification.md": "Product and Requirements Specification",
        "technical-design.md": "Technical Design Document",
        "verification-and-acceptance-plan.md": "Verification and Acceptance Plan",
        "operations-and-slo.md": "Operations and Reliability Specification",
    }
    for filename, document_name in primary_documents.items():
        path = design_path / filename
        if not path.is_file():
            continue
        text = read_text(path)
        if not re.search(r"^\*\*Status:\*\*", text, re.MULTILINE):
            errors.append(f"{document_name} lacks Status header")
        if not re.search(r"^\*\*Owner:\*\*", text, re.MULTILINE):
            errors.append(f"{document_name} lacks Owner header")
        if "## Change Summary" not in text:
            errors.append(f"{document_name} lacks Change Summary")

    adr_dir = design_path / "08-adr"
    adr_files = sorted(adr_dir.glob("ADR-*.md")) if adr_dir.is_dir() else []
    if not adr_files:
        errors.append("missing ADR evidence: expected 08-adr/ADR-*.md")

    arc42_path = design_path / "arc42.md"
    if arc42_path.is_file():
        arc42_text = read_text(arc42_path)
        for headings in ARC42_SECTION_OPTIONS:
            if not any(heading in arc42_text for heading in headings):
                errors.append(f"arc42 missing section: {' / '.join(headings)}")

    requirements_path = design_path / "01-requirements-baseline.md"
    traceability_path = design_path / "11-traceability-matrix.md"
    acceptance_strategy_path = design_path / "10-test-and-acceptance-strategy.md"
    requirement_ids: dict[str, str] = {}
    trace_rows: dict[str, str] = {}
    strategy_scenario_ids: set[str] = set()
    if requirements_path.is_file():
        requirement_ids = markdown_ids(requirements_path)
        if not requirement_ids:
            errors.append("requirements baseline contains no FR-* rows")
    if traceability_path.is_file():
        trace_rows = markdown_ids(traceability_path)
        if not trace_rows:
            errors.append("traceability matrix contains no FR-* rows")
    if acceptance_strategy_path.is_file():
        strategy_text = read_text(acceptance_strategy_path)
        if not re.search(r"^\|\s*(Scenario ID|场景 ID)\s*\|", strategy_text, re.MULTILINE):
            errors.append("acceptance strategy lacks a Scenario ID catalog")
        strategy_scenario_ids = scenario_ids(acceptance_strategy_path)
        if not strategy_scenario_ids:
            errors.append("acceptance strategy contains no named scenario IDs")

    for requirement_id in requirement_ids:
        trace_row = trace_rows.get(requirement_id)
        if trace_row is None:
            errors.append(f"requirement lacks a traceability row: {requirement_id}")
            continue
        columns = [column.strip() for column in trace_row.strip("|").split("|")]
        if len(columns) < 6 or not columns[4] or columns[4] in {"N/A", "TBD"}:
            errors.append(f"requirement lacks an acceptance scenario identifier: {requirement_id}")
            continue
        references = SCENARIO_REFERENCE_PATTERN.findall(columns[4])
        if not references:
            errors.append(f"requirement has no parseable acceptance scenario identifier: {requirement_id}")
        for scenario_id in references:
            if scenario_id not in strategy_scenario_ids:
                errors.append(f"traceability scenario is absent from the acceptance strategy: {requirement_id} -> {scenario_id}")

    review_path = design_path / "13-design-readiness-review.md"
    if review_path.is_file():
        review_text = read_text(review_path)
        ready_for_review = re.search(r"^- \[x\] READY_FOR_HUMAN_REVIEW$", review_text, re.MULTILINE)
        if not ready_for_review:
            errors.append("design-readiness review lacks READY_FOR_HUMAN_REVIEW recommendation")
        if "- [x] REWORK_REQUIRED" in review_text:
            errors.append("design-readiness review marks REWORK_REQUIRED")

    stats = {
        "required_documents": len(REQUIRED_DOCUMENTS),
        "requirements": len(requirement_ids),
        "trace_rows": len(trace_rows),
        "named_acceptance_scenarios": len(strategy_scenario_ids),
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
        "status": "blocked" if errors else ("warnings" if warnings else "ready_for_human_review"),
        "design_package": str(design_path),
        "stats": stats,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
