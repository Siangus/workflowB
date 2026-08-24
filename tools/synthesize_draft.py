import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
root=Path('work/se-workflow'); reg=root/'registry'; wf=root/'workflow-b'; pack=root/'sources/pressman-practitioners-cn'
units=[json.loads(x) for x in (reg/'knowledge-units.jsonl').read_text(encoding='utf-8').splitlines()]
segments=[json.loads(x) for x in (reg/'segments.jsonl').read_text(encoding='utf-8').splitlines()]
inv=json.loads((pack/'inventory.json').read_text(encoding='utf-8'))
now=datetime.now(timezone.utc).isoformat()
domains=['problem-framing','planning','risk','requirements','architecture','design','construction','verification','release','operations','feedback','maintenance','quality','governance','teamwork']
primary=Counter(x['lifecycle_phase'] for x in units)
secondary=Counter(d for x in units for d in x['secondary_domains'])
coverage=[]
for d in domains:
    count=primary.get(d,0); sec=secondary.get(d,0)
    if count>=3 or (count>=2 and sec>=1): cls='usable'
    elif count==2 or sec>=2: cls='stub'
    elif count==1: cls='stub'
    else: cls='none'
    coverage.append({'domain':d,'primary_units':count,'secondary_mentions':sec,'coverage_class':cls,'next_action':'Add specialist book' if cls in ('none','stub') else 'Deepen tailoring and anti-patterns'})
(reg/'coverage.md').write_text('# Coverage\n\n| Domain | Primary | Secondary | Class | Next action |\n|---|---:|---:|---|---|\n'+'\n'.join(f"| `{x['domain']}` | {x['primary_units']} | {x['secondary_mentions']} | `{x['coverage_class']}` | {x['next_action']} |" for x in coverage)+'\n',encoding='utf-8')
with (reg/'merge-log.md').open('w',encoding='utf-8',newline='\n') as f:
    f.write('# Merge Log\n\n## MERGE-0001\n\n')
    f.write(f'- **at:** {now}\n- **source:** `{inv["book_id"]}`\n- **action:** baseline bootstrap\n- **segments indexed:** {len(segments)}\n- **seed knowledge units:** {len(units)}\n- **conflicts:** 0\n- **status:** draft-ready; segment-level deep extraction remains pending\n')
(pack/'integration-report.md').write_text(f'''# Integration Report

- **book_id:** `{inv['book_id']}`
- **generated:** `{now}`
- **files indexed:** {len(inv['files'])}
- **segments indexed:** {len(segments)}
- **seed knowledge units written:** {len(units)}
- **cards directory:** `sources/{inv['book_id']}/cards/`
- **status:** `draft-ready`

## Interpretation
This is a deterministic inventory plus representative lifecycle seed extraction. It proves the registry contract and four-layer synthesis path. It is not a claim that all 76 segments have been deeply read.

## Pending Work
Process each segment through the reading loop, then classify every new card as NEW, REINFORCES, EXTENDS, CONTRADICTS, or OUT_OF_SCOPE.
''',encoding='utf-8')
(wf/'README.md').write_text('''# Workflow B Draft

This draft is generated from the Pressman lifecycle-overview corpus.

## How to read

1. Start with `principles.md`.
2. Select a route in `project-profiles.md`.
3. Follow `sop-state-machine.md` for state transitions.
4. Open the referenced handbook file only when executing a state.

## Status

`draft-ready`, not production-complete. The current version proves structure and control flow; specialist books must deepen requirements, design, testing, operations, and maintenance.
''',encoding='utf-8')
(wf/'principles.md').write_text('''# Invariant Principles

1. Establish a verifiable problem and success signal before committing implementation capacity.
2. Requirements must be owned, prioritized, and testable.
3. Architecture and design decisions must expose trade-offs against quality attributes.
4. Work must be decomposed enough to assign, integrate, and verify.
5. Risk requires probability, impact, response, monitoring signal, and trigger.
6. Change must be controlled through visible baselines and decision records.
7. Defect prevention and early review are cheaper than late discovery.
8. Verification must map to requirements and risk, not merely code execution.
9. Release readiness includes quality evidence, rollback, configuration identity, and operational ownership.
10. Operational feedback must return to planning, requirements, and risk.
''',encoding='utf-8')
(wf/'project-profiles.md').write_text('''# Project Profiles

## Dimensions

| Dimension | Values |
|---|---|
| Team scale | solo / small team / multi-team |
| Requirement certainty | exploratory / clear / contractual |
| Delivery rhythm | one-shot / iterative / continuous |
| Risk | low / medium / high |
| Compliance | none / industry standard / strong regulatory |
| Technical uncertainty | low / medium / high |
| System novelty | greenfield / evolution / migration |
| Feedback latency | short / medium / long |

## Routes

### Lightweight exploratory

**Match:** small team, exploratory need, low compliance, short feedback.

- Merge problem framing and prototype validation.
- Replace full SRS with requirement cards.
- Use a one-page technical design plus API contract.
- Keep version control, automated tests, demoable increment, and rollback.
- Strengthen user-validation gate before broad investment.

### Iterative product delivery

**Match:** small/multi-team, evolving but clear enough needs, continuous or frequent release.

- Maintain a prioritized backlog with acceptance criteria.
- Run architecture walkways at risky milestones.
- Require definition of done, automated regression, observability, and feature flag plan.
- Use lightweight ADRs and release checklist.

### High-assurance delivery

**Match:** high business/safety impact, strong regulatory pressure, long feedback, contractual acceptance.

- Baselined SRS and traceability matrix.
- Formal design review and ADRs.
- Independent review or V&V for critical behavior.
- Configuration audit, approval record, staged deployment, and rollback rehearsal.
- No state exits without objective evidence.
''',encoding='utf-8')
(wf/'tailoring-rules.md').write_text('''# Tailoring Rules

Tailoring changes artifact weight, not accountability. Every reduction needs compensation.

| Rule | Light form | Heavy form | Compensation |
|---|---|---|---|
| Requirements | Requirement card per scenario | SRS + traceability matrix | Acceptance tests and stakeholder sign-off |
| Design | One-page technical plan | Design document + formal review | ADR and executable architecture slice |
| Planning | Rolling-wave board | Task network + earned value | Critical-path review at gates |
| Risk | Top-ten table | Quantified risk model | Trigger-based escalation |
| Review | Checklist peer review | Formal inspection | Escape-rate metrics |
| Testing | Thin-slice E2E + regression | Independent/system V&V | Risk-based coverage and staging |
| Release | Deploy checklist | Approval package + audit | Immutable build and rollback drill |

Never remove: problem statement, decision ownership, version control, verification of protected behavior, configuration identity, rollback/recovery, or operational feedback.
''',encoding='utf-8')
states=[
('problem-framing','Problem Framing','Establish the problem, users, value, constraints, and kill criteria.',['Business opportunity or pain exists.','Decision owner is identified.'],['Frame the problem.','Define success measures.','Identify constraints/stakeholders.','Run feasibility check.'],['Problem statement','Success criteria','Proceed/pivot/stop'],['Success measures are observable.','Feasibility conclusion has evidence.','Top risks named.'],['Product owner','Engineer','Business owner'],['Value/scope unstable'],['prototype-validation','planning-and-risk'],'handbook/management.md'),
('planning-and-risk','Planning and Risk','Create a capacity-aware plan with explicit uncertainty responses.',['Problem framed.'],['Decompose scope.','Estimate ranges.','Build task network.','Prepare risk table.'],['Plan','Risk register','Decision log'],['Plan fits capacity.','High risks have triggers.','Critical path known.'],['Project lead','Engineer lead'],['Schedule/risk invalid'],'requirements-clarification','handbook/management.md'),
('requirements-clarification','Requirements Clarification','Define verifiable scope and acceptance intent.',['Problem and stakeholders known.'],['Elicit scenarios/constraints.','Prioritize conflicts.','Define acceptance criteria.'],['Requirement cards/SRS','Out-of-scope list','Open issues'],['Requirements verifiable.','Owner confirms priority.','Coverage maps to scenarios.'],['Product owner','Engineer','Tester'],['Unstable value/scope'],'architecture-and-design','handbook/requirements.md'),
('architecture-and-design','Architecture and Design','Select a coherent structure satisfying functional and quality needs.',['Verifiable scope exists.'],['Design data/architecture/interfaces/UX.','Record key trade-offs.','Define module contracts.'],['Design model','ADR','Interface contracts'],['Traceability exists.','Quality attributes addressed.','Interfaces testable.'],['Architect/engineer','Reviewer','UX'],['Quality attributes fail'],'construction-and-integration','handbook/design.md'),
('construction-and-integration','Construction and Integration','Implement maintainable increments under configuration control.',['Approved design slice.'],['Implement behind interfaces.','Review changes.','Integrate continuously.','Control versions/baselines.'],['Source changes','Review record','Integrated build'],['CI passes.','Review findings closed.','No unauthorized dependency change.'],['Engineer','Reviewer','Release engineer'],['Design cannot support requirement'],'verification','handbook/construction.md'),
('verification','Verification','Demonstrate intended behavior and discover failure conditions.',['Testable increment exists.'],['Execute unit/integration/scenario tests.','Apply boundary/negative cases.','Track defects to exit criteria.'],['Test results','Coverage evidence','Defect triage'],['Protected behavior passes.','Known failures dispositioned.','Regression suite green.'],['Engineer','Tester','Risk owner'],['Requirements/design defect'],'release-readiness','handbook/testing.md'),
('release-readiness','Release Readiness','Confirm safe, recoverable, auditable delivery.',['Verification exit met.'],['Complete release checklist.','Audit build/configuration.','Rehearse rollback.','Obtain approvals.'],['Release candidate','Approval record','Rollback procedure'],['Build identity verified.','Monitoring ready.','Approval complete.'],['Release manager','Operations','Approver'],['Release blocker'],'operations-and-feedback','handbook/governance.md'),
('operations-and-feedback','Operations and Feedback','Run, observe, support, and learn from production.',['Release accepted.'],['Monitor SLIs.','Support incidents.','Capture usage/cost/defect signals.','Feed backlog/planning.'],['Dashboard','Incident record','Improvement backlog'],['Signals reach owners.','Recovery tested.','Learning becomes action.'],['Operations','Product owner','Engineer'],['Systemic instability'],'planning-and-risk','handbook/operations.md')]
out=['# SOP State Machine','','Legend: each state is a control plane. Handbook links contain methods; do not expand this file into a manual.','']
for sid,name,goal,entry,acts,outp,exits,roles,fallback,next_state,handbook in states:
    gates = ["Objective evidence: " + item for item in exits]
    out += [f'## {name}',f'- **state_id:** `{sid}`',f'- **goal:** {goal}',f'- **entry_criteria:** '+('; '.join(entry)),f'- **activities:** '+('; '.join(acts)),f'- **outputs:** '+('; '.join(outp)),f'- **exit_criteria:** '+('; '.join(exits)),f'- **quality_gates:** '+('; '.join(gates)),f'- **roles:** '+('; '.join(roles)),f'- **fallback:** {fallback}',f'- **next_state:** `{next_state}`',f'- **handbook:** `{handbook}`','']
(wf/'sop-state-machine.md').write_text('\n'.join(out),encoding='utf-8')
for domain,file,title in [('requirements','requirements.md','Requirements'),('architecture','design.md','Architecture and Design'),('construction','construction.md','Construction'),('verification','testing.md','Testing'),('release','governance.md','Release and Governance'),('planning','management.md','Planning, Risk, Problem Framing'),('operations','operations.md','Operations and Feedback')]:
    related=[x for x in units if x['lifecycle_phase']==domain or domain in x['secondary_domains']]
    lines=[f'# {title} Handbook','', '| ID | Method | Purpose | Tailoring | Source |','|---|---|---|---|---|']
    for x in related:
        tail=x['tailoring'].get('light','light') if isinstance(x['tailoring'],dict) else str(x['tailoring'])
        lines.append(f"| `{x['ku_id']}` | [{x['title']}](../../sources/{x['book_id']}/cards/{x['ku_id']}.md) | {x['purpose']} | {tail} | `{x['source_locator']}` |")
    if len(related)==1: lines += ['','> This domain currently has only seed coverage. Add a specialist source before using it for high-risk work.']
    (wf/'handbook'/file).write_text('\n'.join(lines)+'\n',encoding='utf-8')
(wf/'templates'/'requirement-card-template.md').write_text('''# Requirement Card\n\n- **ID:** REQ-\n- **Title:**\n- **User / beneficiary:**\n- **Problem / job:**\n- **Outcome measure:**\n- **Scenario:** Given..., when..., then...\n- **Acceptance criteria:**\n  - [ ] Observable result\n  - [ ] Boundary condition\n  - [ ] Failure/fallback\n- **Priority / owner:**\n- **Non-goals:**\n- **Risks / open questions:**\n''',encoding='utf-8')
(wf/'templates'/'design-decision-template.md').write_text('''# Design Decision\n\n- **ID:** ADR-\n- **Status:** proposed / accepted / replaced\n- **Context:**\n- **Decision:**\n- **Alternatives:**\n- **Consequences:**\n- **Quality attributes affected:**\n- **Reversibility / migration:**\n- **Evidence / spike:**\n''',encoding='utf-8')
(wf/'templates'/'release-checklist-template.md').write_text('''# Release Checklist\n\n- [ ] Build identifier recorded\n- [ ] Source revision matches release\n- [ ] CI/regression evidence attached\n- [ ] Security/privacy checks complete\n- [ ] Migration reviewed\n- [ ] Rollback rehearsed\n- [ ] Monitoring/dashboard ready\n- [ ] Support owner assigned\n- [ ] Approvals recorded\n''',encoding='utf-8')
print(json.dumps({'coverage':len(domains),'workflow_files':sum(1 for p in wf.rglob('*') if p.is_file())},ensure_ascii=False))



