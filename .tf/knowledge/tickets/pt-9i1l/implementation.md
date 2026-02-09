# Implementation: pt-9i1l

## Summary
Added a new "Follow-ups Scan" procedure to the tf-planning skill documentation. This procedure describes the `/tf-followups-scan` command behavior, flags, and safety defaults.

## Files Changed
- `.pi/skills/tf-planning/SKILL.md` - Added new procedure section after "Follow-up Creation"

## Key Decisions
- Placed the new procedure immediately after "Follow-up Creation" to show the relationship between single-ticket and scan modes
- Used the existing procedure format with clear Purpose/Input/Flags/Steps structure
- Referenced `workflow.knowledgeDir` from settings.json as required
- Defined "implemented ticket" heuristic: must have both `implementation.md` and `review.md`
- Made dry-run the default for safety, requiring explicit `--apply` flag
- Documented scan mode as complementary to the existing single-ticket follow-up creation

## Implementation Details

### New Procedure: Follow-ups Scan

The procedure includes:
1. **Configuration**: Resolves `workflow.knowledgeDir` from settings.json
2. **Discovery**: Scans ticket artifact directories for implemented tickets
3. **Heuristic**: Tickets must have both `implementation.md` and `review.md` to be considered
4. **Flags**:
   - `--dry-run` (default) - Preview without creating
   - `--apply` - Actually create tickets
   - `--since <date>` - Filter by implementation date
   - `--ticket <id>` - Scan specific ticket
   - `--limit <n>` - Limit number of tickets
5. **Safety defaults**: Dry-run by default, explicit opt-in required, skips incomplete tickets
6. **Output**: Creates `scan-followups.md` summary when in apply mode
7. **Relationship**: Clearly documents how scan mode delegates to single-ticket follow-up creation

## Tests Run
- Verified SKILL.md syntax is valid markdown
- Confirmed new procedure follows existing document structure

## Verification
- Read the updated SKILL.md to confirm the procedure is properly formatted
- Check that existing "Follow-up Creation" procedure remains intact
