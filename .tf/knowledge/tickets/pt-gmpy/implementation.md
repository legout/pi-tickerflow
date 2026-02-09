# Implementation: pt-gmpy

## Summary
Enhanced `/tf-backlog` prompt to incorporate session-linked plan and spike documents as inputs for backlog ticket generation. This fulfills the requirement to use session artifacts as additional context when generating tickets.

## Changes Made

### File: `prompts/tf-backlog.md`

#### 1. Added Phase B: Session Input Incorporation (lines ~82-110)
New section after Phase A (Session-Aware Topic Resolution) that:
- **B.1**: Reads plan document if `session.plan` is set
  - Extracts requirements from `## Requirements`
  - Extracts constraints from `## Constraints`
  - Checks plan status from frontmatter
  - Warns if plan not approved
- **B.2**: Reads spike documents if `session.spikes[]` is non-empty
  - Extracts summary/key findings
  - Extracts recommendations
  - Notes constraints/risks
- **B.3**: Incorporates extracted content into ticket descriptions
  - Adds plan requirements to `## Context` (briefly)
  - Adds constraints from plan/spikes to `## Constraints`
  - Uses spike findings to inform implementation approach
  - Gracefully handles missing/unreadable docs with warnings
- **B.4**: Tracks inputs used for final summary

#### 2. Updated Output Section (lines ~270-285)
Added "Inputs Used Summary" format:
```
[tf] Inputs: seed={topic-id} plan={plan-id|none} spikes={count} [{spike-id1}, ...]
```

With examples for:
- Plan + spikes present
- No plan, no spikes
- Partial read failures (warnings)

#### 3. Added Seed with Session Inputs Template (lines ~315-345)
New template showing how tickets should reference plan and spikes:
- Context includes plan requirements (1-2 sentences)
- Context references spike findings
- Constraints section includes plan/spike constraints
- References section lists seed, plan, and spikes

#### 4. Enhanced Session Finalization (step 11)
Added `backlog.inputs_used` object to session archive:
```json
{
  "seed": "{topic-id}",
  "plan": "{plan-id or null}",
  "plan_status": "{approved|draft|missing}",
  "spikes": ["{spike-id-1}", "{spike-id-2}"],
  "spikes_read": 2,
  "spikes_missing": []
}
```

## Acceptance Criteria Verification

| Criterion | Status | Implementation |
|-----------|--------|----------------|
| If session.plan is set, read plan doc | ✅ | Phase B.1 |
| Incorporate requirements/constraints | ✅ | Phase B.3 (context & constraints) |
| If session.spikes[] non-empty, read spike docs | ✅ | Phase B.2 |
| Incorporate spike findings | ✅ | Phase B.3 (context & recommendations) |
| Output "inputs used" summary | ✅ | Output section format + examples |
| Keep tickets self-contained | ✅ | Brief incorporations, no long pastes |
| Conservative: warn on missing docs | ✅ | Phase B.3 error handling |

## Design Decisions

1. **Brief incorporations**: Tickets remain self-contained with 1-2 sentence references rather than full document pastes
2. **Conservative error handling**: Continue with seed-only if plan/spike docs missing, with warnings
3. **Template examples**: Added explicit "Seed with Session Inputs" template showing best practices
4. **Audit trail**: Session archive captures what inputs were used for traceability

## Files Changed
- `prompts/tf-backlog.md` - Enhanced with session input incorporation

## No Tests Required
This is a prompt/documentation change; no code to test. The behavior will be validated by:
1. Creating a planning session with plan and/or spikes
2. Running `/tf-backlog` and verifying the inputs summary appears
3. Checking created tickets reference plan/spike content appropriately
