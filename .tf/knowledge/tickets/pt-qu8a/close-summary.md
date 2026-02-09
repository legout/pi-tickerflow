# Close Summary: pt-qu8a

## Status
CLOSED

## Implementation Summary
Changed the serial `tf ralph start --progress` counter total to reflect the number of ready tickets, not `max_iterations` (default 50).

## Changes Made
- `tf_cli/ralph.py`: Modified to compute ready tickets count once at loop start
  - Added Union import for type hints
  - Updated ProgressDisplay.total to accept Union[int, str]
  - Compute ready_tickets_count once before the while loop
  - Show "?" placeholder when listing fails

## Commit
7c5cd14 - pt-qu8a: Compute correct progress total for tf ralph --progress

## Testing
- 22 progress display tests: PASSED
- 82 ralph state/invocation/logging tests: PASSED
- Total: 104 tests passed

## Quality Metrics
- Critical: 0
- Major: 0
- Minor: 0

## Verification
- [x] Progress display total derived from ready tickets count
- [x] Computed once at loop start (not per-iteration)
- [x] Shows "?" on listing failure (not 50)
- [x] No behavior change when --progress not used
