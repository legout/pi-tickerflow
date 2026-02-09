# Implementation: pt-4hyo

## Summary
Test + document `/tf-followups-scan` (dry-run + apply) with sample tickets.

## Files Changed
- `docs/commands.md` - Added `/tf-followups-scan` command reference
- `docs/tf-followups-scan-manual-test.md` - Created comprehensive manual test recipe

## Key Changes

### docs/commands.md
Added new section for `/tf-followups-scan` under "Ticket Creation Commands":
- Full command syntax and arguments
- Description of behavior (scans ticket artifacts, dry-run default)
- Idempotency note (second run does nothing)
- Output artifacts specification
- Usage examples
- Sample output format

### docs/tf-followups-scan-manual-test.md (new file)
Created comprehensive manual test recipe with 6 test cases:

1. **Test Case 1**: Dry-Run Mode - verifies no side effects
2. **Test Case 2**: Apply Mode - verifies actual ticket creation and file writes
3. **Test Case 3**: Idempotency - verifies second run does nothing
4. **Test Case 4**: No review.md - graceful handling when review is missing
5. **Test Case 5**: Empty Review - "none needed" record creation
6. **Test Case 6**: Multiple Tickets - batch processing verification

Each test case includes:
- Purpose statement
- Step-by-step instructions
- Verification checklist
- Cleanup instructions

Also includes:
- Prerequisites section
- Regression checklist
- Notes for maintainers

## Acceptance Criteria Coverage

| Criterion | Status | Notes |
|-----------|--------|-------|
| Update docs with usage and examples | ✅ | Added to commands.md |
| Add manual test recipe | ✅ | New dedicated test doc |
| Document dry-run then apply workflow | ✅ | Test Case 1 & 2 |
| Document idempotency | ✅ | Test Case 3 + explicit note in commands.md |

## Decisions Made

1. **Documentation location**: Added to existing `docs/commands.md` rather than creating a separate file, keeping command reference centralized.

2. **Test document scope**: Created a dedicated manual test file rather than embedding in commands.md to keep the command reference concise while providing detailed test procedures.

3. **Idempotency documentation**: Highlighted prominently in both the command reference and test case, as it's a key safety feature.

## Verification

To verify the documentation:
1. Check `docs/commands.md` contains the new `/tf-followups-scan` section
2. Check `docs/tf-followups-scan-manual-test.md` exists and contains all 6 test cases
3. Verify markdown renders correctly
