# Project Design Package Template

Copy this directory into the project repository before construction. Keep documents concise, but do not omit a document when its question is relevant. Mark genuinely irrelevant sections as `Not applicable: <reason>`.

Construction is blocked until `13-design-readiness-review.md` records `APPROVED` or `APPROVED_WITH_RISKS`.

`arc42.md` is required. It is the coherent architecture narrative; the numbered documents provide detailed evidence and traceability.

Before approval, run `scripts/validate_project_design_package.py <design-package-path>` from the Workflow B Skill directory. The validator checks the required artifacts, arc42 sections, ADR presence, requirement-to-test trace rows, and the review decision. It does not replace human review of the design evidence.
