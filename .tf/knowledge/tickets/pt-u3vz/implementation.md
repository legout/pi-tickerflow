# Implementation: pt-u3vz

## Summary
Added comprehensive unit tests for Ralph progress total computation to prevent regressions where progress total reverts to `maxIterations` (50) instead of actual ready ticket count.

## Files Changed
- `tests/test_ralph_progress_total.py` (new) - 7 unit tests for progress total functionality

## Key Decisions
- Created a new test file rather than adding to existing tests to keep concerns separate
- Used extensive mocking to avoid shelling out to `pi` or `tk` commands
- Tests cover both positive cases (correct total) and negative cases (regression detection)
- Named tests explicitly to indicate regression testing purpose

## Tests Added

### TestRalphProgressTotalComputation
1. `test_progress_total_matches_ready_ticket_count` - Verifies total equals actual count, not 50
2. `test_progress_total_with_five_tickets` - Verifies [1/5] for 5 tickets
3. `test_progress_shows_placeholder_when_listing_fails` - Verifies '?' on exception
4. `test_progress_shows_question_when_empty_list` - Verifies '?' for empty list
5. `test_no_progress_without_flag` - Verifies ProgressDisplay not created without --progress

### TestProgressTotalRegression
6. `test_progress_not_shows_fifty_for_small_backlog` - Critical regression test for [*/50]
7. `test_progress_single_ticket_not_shows_fifty` - Single ticket should show [1/1], not [1/50]

## Test Results
```
7 passed in 0.88s
```

All tests pass and do not shell out to external commands. Full ralph test suite:
```
111 passed in 1.24s
```

## Verification
- Run: `python -m pytest tests/test_ralph_progress_total.py -v`
- All 7 new tests pass
- No regressions in existing 104 ralph tests
