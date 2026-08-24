# L3 Provenance Guide

L3 is loaded only for traceability, disagreement, audit, or deep study.

```text
L1/L2 method
→ knowledge-unit ID
→ registry/knowledge-units.jsonl
→ sources/<book-id>/cards/<KU-ID>.md
→ source locator in the original book segment
```

Use `registry/conflicts.jsonl` when two methods are context-dependent or materially disagree. Use `registry/merge-log.md` to understand when a source entered B. Do not load all source cards during ordinary state execution.
