# Implementation: pt-7l5c

## Summary
Updated `/tf-plan` command to support session-aware plan attachment with automatic "Inputs / Related Topics" section generation and cross-linking.

## Files Changed

### 1. `skills/tf-planning/SKILL.md`
- Updated "Procedure: Plan Interview (Planner)" to include session-aware steps
- Added Step 1: Check for active planning session
- Updated Step 4 (was 3): Added "Inputs / Related Topics" section template to plan.md
- Added Step 6: Update active session with plan ID (overwrites prior plan)
- Added Step 7: Cross-link seed↔plan in sources.md files

### 2. `prompts/tf-plan.md`
- Updated description to mention session attachment feature
- Expanded execution section with detailed session-aware steps
- Added "Session Behavior" section explaining with/without active session
- Updated "Output" section to reflect session artifacts
- Added examples for "Inputs / Related Topics" section format

## Key Decisions

1. **Session detection first**: The plan interview procedure now checks for an active session before creating the plan, ensuring the "Inputs / Related Topics" section is populated during plan creation.

2. **Overwrite semantics**: When a session already has a plan, the new plan overwrites the prior one (as specified in acceptance criteria). This allows iterative planning without session pollution.

3. **Dedup for sources.md**: Cross-links use deduplication logic - links are only added if not already present, ensuring idempotency.

4. **Consistent with spike pattern**: The implementation follows the same pattern established in "Research Spike" procedure for session attachment and cross-linking.

## Verification

### Check SKILL.md changes:
```bash
grep -A 5 "Inputs / Related Topics" skills/tf-planning/SKILL.md
```

### Check prompt changes:
```bash
grep -A 10 "Session Behavior" prompts/tf-plan.md
```

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| Active session updated with `plan: <plan-id>` (overwriting prior plan) | ✅ Implemented in SKILL.md Step 6 |
| Generated plan includes "Inputs / Related Topics" section | ✅ Implemented in SKILL.md Step 4 |
| Section lists root seed and all session spikes | ✅ Documented in template |
| Seed `sources.md` and plan `sources.md` are cross-linked | ✅ Implemented in SKILL.md Step 7 |
| Emits one-line notice when auto-attaching | ✅ Documented in SKILL.md Step 6 |
| Behavior unchanged when no active session exists | ✅ Documented in prompt Session Behavior section |

## Notes

- The implementation is documentation-based (SKILL.md and prompt files) as the TF system uses these as the source of truth for command behavior
- No code changes were required as the session storage API (`session_store.py`) already supports `set_plan_for_session()`
- The cross-linking in sources.md uses the existing dedup pattern from the Research Spike procedure
