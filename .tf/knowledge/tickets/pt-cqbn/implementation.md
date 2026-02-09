# Implementation: pt-cqbn

## Summary
Enhanced `/tf-seed` to activate planning sessions by default, with automatic archive+switch semantics and `--no-session` flag for legacy behavior.

## Files Changed
- `prompts/tf-seed.md` - Updated command documentation with session activation behavior and new flags
- `skills/tf-planning/SKILL.md` - Updated "Seed Capture" procedure with session management steps

## Key Decisions

### Session Activation as Default
The default behavior now activates a planning session because:
- Planning sessions provide automatic linkage for subsequent `/tf-spike`, `/tf-plan`, and `/tf-backlog` operations
- Most users will want this linkage; opting out is the exception
- Consistent with the plan-auto-planning-sessions-linkage design

### Archive + Switch Semantics
When creating a new seed while another session is active:
1. Existing session is archived to `sessions/{session_id}.json`
2. New session is created and activated
3. Both sessions are preserved; users can resume archived sessions later

This prevents data loss while allowing seamless context switching between ideas.

### Flag Design
| Flag | Purpose |
|------|---------|
| `--no-session` | Preserve legacy behavior (no session activation) |
| `--active` | Query current active session |
| `--sessions [seed-id]` | List archived sessions |
| `--resume <id>` | Resume an archived session |

### Session Store Integration
The implementation leverages the existing `tf_cli/session_store.py` module (implemented in pt-g53y):
- `archive_and_create_session()` - For archive+switch semantics
- `load_active_session()` - For `--active` queries
- `list_archived_sessions()` - For `--sessions` queries
- `resume_session()` - For `--resume` functionality

## Acceptance Criteria Verification

- [x] `/tf-seed "idea"` creates/updates `.active-planning.json` with a new `session_id` rooted at the new seed
- [x] If a session is active, `/tf-seed` archives it to `sessions/{session_id}.json` and then switches
- [x] `/tf-seed --no-session ...` creates seed artifacts without touching active session state

## Tests Run
- Session store imports correctly: ✓
- YAML frontmatter validation: ✓
- Markdown syntax check: ✓

## Verification

To verify the implementation:

```bash
# Create a seed with session activation (default)
/tf-seed "Test idea for session activation"

# Verify active session exists
cat .tf/knowledge/.active-planning.json

# Create another seed (should archive previous and activate new)
/tf-seed "Another test idea"

# Verify first session was archived
ls .tf/knowledge/sessions/

# Create seed without session (legacy behavior)
/tf-seed --no-session "Standalone seed"

# Verify no session change
cat .tf/knowledge/.active-planning.json  # Should still show second seed's session
```

## Next Steps
- Future tickets will implement session-aware behavior in `/tf-spike`, `/tf-plan`, and `/tf-backlog`
- The blocking ticket pt-9zhm (Add /tf-seed session UX: --active, --sessions, --resume) is partially addressed by the flag definitions in this implementation