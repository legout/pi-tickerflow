# Implementation: ptw-cn2e

## Summary
Added ticket linking support in `/tf-backlog` using `tk link`. Links are symmetric and help discoverability/grouping for related work that is not strictly dependent.

## Files Changed

### 1. prompts/tf-backlog.md
- Added `--no-links` option to Usage and Arguments sections
- Added new step 8: "Link related tickets" with linking criteria and `tk link` command
- Updated Output section to mention links

### 2. skills/tf-planning/SKILL.md
- Updated step 9 (dependencies) to be more detailed
- Added new step 10: "Link related tickets" procedure with:
  - Linking criteria (same component + adjacent, title similarity)
  - Conservative approach (under-linking preferred)
  - Max 2-3 links per ticket
  - `tk link <id> <id>` command usage
- Updated backlog.md format documentation to clarify Links column

## Key Decisions

1. **Conservative linking**: Under-linking is preferred to over-linking as per ticket constraints
2. **Linking criteria**:
   - Same component tags + adjacent in creation order
   - Title similarity (significant shared words)
3. **Opt-out**: Added `--no-links` flag for users who want to skip automatic linking
4. **Symmetric links**: Uses `tk link` which creates bidirectional relationships (unlike deps which are directional)

## Linking Criteria Documented

- Same component + adjacent in creation order
- Title similarity (e.g., "component classifier" and "component tags" share "component")
- Max 2-3 links per ticket to avoid noise

## Tests Run
- Syntax check on modified files
- Ruff linting (pre-existing issues only, no new issues introduced)

## Verification
To verify the implementation:
1. Run `/tf-backlog <topic>` and confirm tickets are created
2. Check that related tickets are linked via `tk link`
3. Verify `backlog.md` includes Links column
4. Run `/tf-backlog <topic> --no-links` to confirm opt-out works
