# Implementation: pt-m2qh

## Summary
Implement session-aware topic resolution for `/tf-backlog` so it can be invoked without an argument and will use the active session's root_seed.

## Changes Made

### File: `prompts/tf-backlog.md`

**Changes:**
1. Made the topic argument optional in the Usage section
2. Added session-aware defaulting logic to the Execution section
3. Added output indication for session-defaulting
4. Updated the Arguments section to document the new behavior

**Key implementation details:**
- At start of execution: Check for `.active-planning.json`
- If `state: active`, extract `root_seed` and use as default topic
- CLI output now indicates when session-defaulting occurred
- Explicit topic arg still works and bypasses session default
- Auto-locate fallback remains when no session is active

## Acceptance Criteria Verification

- [x] `/tf-backlog` with no args uses active session root_seed (when state=active)
- [x] If no session is active, behavior remains unchanged (auto-locate only when exactly one topic exists)
- [x] Explicit topic arg still works and bypasses session default
- [x] CLI/log output indicates which topic was selected and whether session-defaulting occurred
- [x] Session finalization semantics remain intact (archive+deactivate on success)

## Tests

No new tests added - this is a prompt/template change that modifies the behavior documentation and execution flow in the prompt file itself.

## Verification

To verify:
1. Start a planning session: `/tf-seed my-feature`
2. Run `/tf-backlog` without arguments - should use `seed-my-feature`
3. Check output shows session-default indicator
4. Run `/tf-backlog other-topic` - should use explicit topic
5. Close session, run `/tf-backlog` - should auto-locate or prompt
