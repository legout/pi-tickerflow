# Fixes: pt-az2p

## Summary
Applied quick fixes to address Major and Minor review findings. All Critical issues were already resolved (none found).

## Issues Fixed

### Major (1)
1. **Header format inconsistency** (`docs/deprecation-policy.md:1`)
   - Changed: `# Deprecation Policy: TF Legacy Namespaces`
   - To: `# Deprecation Policy for TF Legacy Namespaces`
   - Rationale: Match project convention (simpler title format without colon subtitle)

### Minor (2)
2. **Incorrect file entry in table** (`docs/deprecation-policy.md`)
   - Removed: `project_bundle_new.py` → `project_bundle.py` entry
   - Added: `update_new.py` → `update.py` entry
   - Rationale: `project_bundle.py` already exists without `_new` suffix; `update_new.py` was missing from the list

3. **sed pattern too restrictive** (`docs/deprecation-policy.md:230`)
   - Changed: `[a-z_]*` to `[a-z0-9_]*`
   - Changed: `*.py` to `tf_cli/*.py`
   - Rationale: Future-proof for module names with numbers; target correct directory

## Issues Not Fixed (Intentionally)

### Minor (4 remaining)
- Date format consistency - ISO format is preferred for machine readability
- Unchecked milestone items - These are intentionally unchecked as they represent future work
- Related tickets table clarification - Will be updated when pt-g42s status changes

### Warnings (5)
- Hard-coded dates becoming stale - Will update manually as phases complete
- Rollback plan lacks owner - To be addressed in operational runbook (separate ticket)
- Unchecked milestone items - These represent actual work items for follow-up tickets
- Hard-coded module imports in cli.py - Will be addressed in CLN-10 (pt-g42s)
- Dual command namespace maintenance - To be addressed during soft deprecation phase

### Suggestions (7)
- Add document to index - Can be done post-approval
- Metrics tracking - Requires monitoring infrastructure (follow-up ticket)
- FAQ section - Can be added based on user questions
- Version tagging - Consider for future policy updates
- Deprecation warning examples - Can be added when implementing warnings
- Feature flags - Consider if rollback concerns emerge

## Files Modified
- `docs/deprecation-policy.md` - Applied 3 fixes

## Verification
- Reviewed document structure remains intact
- All acceptance criteria still satisfied
- Timeline and removal criteria unchanged
