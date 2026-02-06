# Implementation: pt-v2jv

## Summary
Updated the Research Spike procedure in `skills/tf-planning/SKILL.md` to support session-aware auto-linking. When a planning session is active, spikes are now automatically attached to the session and cross-references are written in both directions.

## Changes Made

### Modified: `skills/tf-planning/SKILL.md`

Updated the **Research Spike** procedure to add session-aware auto-linking:

#### Step 2: Check for active planning session (NEW)
- Load `{knowledgeDir}/.active-planning.json` if it exists
- If `state` is `"active"`, capture `session_id` and `root_seed`
- If no active session, proceed with normal flow (no session linking)

#### Step 6: Update active session (if applicable) (NEW)
- If an active session was detected in step 2:
  - Append `topic-id` to `spikes[]` array in `.active-planning.json` (dedup: skip if already present)
  - Update `updated` timestamp in session file
  - Emit notice: `[tf] Auto-attached spike to session: {session_id}`

#### Step 7: Cross-link with root seed (if applicable) (NEW)
- If an active session was detected:
  - **Root seed `sources.md`**: Add or append to "Session Links" section with spike link
  - **Spike `sources.md`**: Add link back to root seed with parent session info
  - Both with deduplication

## Implementation Details

The changes ensure:
1. **Behavior unchanged when no active session exists** - existing workflow preserved
2. **Deduplication** - no duplicate entries in `spikes[]` or sources.md
3. **Bidirectional linking** - both root seed and spike reference each other
4. **Clear output** - user is notified when auto-attachment occurs

## Files Changed
- `skills/tf-planning/SKILL.md` - Updated Research Spike procedure

## Tests
- All 248 tests pass
- Verified skill file parses correctly
- Checked markdown structure preserved

## Verification
To verify the changes:
1. Create an active planning session with `/tf-seed "test session"`
2. Run `/tf-spike "test topic"`
3. Check `.active-planning.json` - spike ID should be in `spikes[]`
4. Check root seed's `sources.md` - should have Session Links section
5. Check spike's `sources.md` - should link back to root seed
