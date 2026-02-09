# Research: pt-gmpy

## Status
Research complete. This is an internal workflow enhancement requiring no external research.

## Context Reviewed

### Session Structure
Located session schema from `.tf/knowledge/sessions/*.json`:
```json
{
  "schema_version": 1,
  "session_id": "...",
  "state": "active|archived|completed|error",
  "root_seed": "seed-topic-id",
  "spikes": ["spike-topic-id-1", "spike-topic-id-2"],
  "plan": "plan-topic-id or null",
  "backlog": { ... }
}
```

### Spike Document Structure
From `spike-pi-non-interactive-logs/spike.md`:
- Contains `## Summary` section with key findings
- Contains `## Key Findings` with numbered items
- Contains `## Recommendation` section
- Useful for extracting constraints/requirements for tickets

### Plan Document Structure
From `plan-kb-management-cli/plan.md`:
- Contains frontmatter with `status: approved`
- Contains `## Requirements` section
- Contains `## Constraints` section  
- Contains `## Work Plan (phases / tickets)`
- Useful for extracting requirements and work phases

### Current tf-backlog Prompt
Read `/prompts/tf-backlog.md`:
- Already has "Session-Aware Topic Resolution (Phase A)" for defaulting topic
- Has session finalization (step 11)
- Missing: reading plan/spike docs and incorporating into ticket context
- Missing: "inputs used" summary output

## Implementation Plan
1. Add Phase B: "Session Input Incorporation" after Phase A
2. Read plan.md if `session.plan` is set, extract requirements/constraints
3. Read spike.md files if `session.spikes[]` non-empty, extract key findings
4. Add guidance on incorporating these into ticket descriptions
5. Add "inputs used" summary to output requirements

## Sources
- `.tf/knowledge/sessions/seed-when-executing-tf-backlog-in-an-active-s@2026-02-07T14-19-43Z.json`
- `.tf/knowledge/topics/spike-pi-non-interactive-logs/spike.md`
- `.tf/knowledge/topics/plan-kb-management-cli/plan.md`
- `/prompts/tf-backlog.md` (current implementation)
