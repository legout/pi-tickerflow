# Implementation: ptw-f1

## Summary
Added documentation for the `--no-deps` flag in the Backlog Generation procedure introduction and step 1 (detect mode).

## Files Changed
- `skills/tf-planning/SKILL.md` - Added `--no-deps` flag documentation

## Changes Made

### 1. Procedure Introduction (after "Input" section)
Added a new **Flags** subsection:
```markdown
**Flags**:
- `--no-deps` - Skip automatic dependency inference (default: dependencies are inferred)
```

### 2. Step 1 (Detect mode)
Added a note at the end of the detect mode step:
```markdown
- Note: Use `--no-deps` flag to skip automatic dependency inference (see step 9)
```

## Acceptance Criteria Verification
- [x] Add note about `--no-deps` flag in the Backlog Generation procedure introduction
- [x] Mention flag in step 1 (detect mode) or early in the procedure
- [x] Ensure implementers are aware of the option before they start creating tickets

## Tests Run
- N/A - Documentation change only

## Verification
- Verified the `--no-deps` flag is now documented early in the procedure
- Flag reference in step 1 points to step 9 for full details
