# Close Summary: pt-np39

## Status
**CLOSED** ✅

## Commit
`41133ff` pt-np39: Rename *_new.py modules to stable names

## Summary
Successfully renamed all transitional `*_new.py` modules to stable names and updated all references throughout the codebase.

## Files Changed
### Source Modules (13 renamed)
- tf_cli/agentsmd_new.py → tf_cli/agentsmd.py
- tf_cli/backlog_ls_new.py → tf_cli/backlog_ls.py
- tf_cli/doctor_new.py → tf_cli/doctor.py
- tf_cli/init_new.py → tf_cli/init.py
- tf_cli/login_new.py → tf_cli/login.py
- tf_cli/next_new.py → tf_cli/next.py
- tf_cli/priority_reclassify_new.py → tf_cli/priority_reclassify.py
- tf_cli/ralph_new.py → tf_cli/ralph.py
- tf_cli/setup_new.py → tf_cli/setup.py
- tf_cli/sync_new.py → tf_cli/sync.py
- tf_cli/tags_suggest_new.py → tf_cli/tags_suggest.py
- tf_cli/track_new.py → tf_cli/track.py
- tf_cli/update_new.py → tf_cli/update.py

### Test Files (5 renamed)
- tests/test_init_new.py → tests/test_init.py
- tests/test_next_new.py → tests/test_next.py
- tests/test_sync_new.py → tests/test_sync.py
- tests/test_track_new.py → tests/test_track.py
- tests/test_update_new.py → tests/test_update.py

### Updated References
- tf_cli/cli.py - 16 import statements updated
- tf_cli/new_cli.py - 13 imports + 13 dispatch calls updated
- tf_cli/setup.py - 1 import + 1 call updated
- tf_cli/component_classifier.py - docstring updated
- tests/test_priority_reclassify.py - import + patch decorators updated
- tests/test_doctor_version.py - import updated
- tests/test_doctor_version_integration.py - import updated
- tests/test_json_capture.py - import updated

## Test Results
**579 passed** - All tests pass after implementation and fixes.

## Review Summary
| Severity | Count | Status |
|----------|-------|--------|
| Critical | 8 | All fixed |
| Major | 1 | Acknowledged |
| Minor | 1 | Fixed |
| Warnings | 1 | Follow-up ticket suggested |
| Suggestions | 1 | Follow-up ticket suggested |

## Artifacts
- `.tf/knowledge/tickets/pt-np39/implementation.md`
- `.tf/knowledge/tickets/pt-np39/review.md`
- `.tf/knowledge/tickets/pt-np39/fixes.md`
- `.tf/knowledge/tickets/pt-np39/review-general.md`
- `.tf/knowledge/tickets/pt-np39/review-spec.md`
- `.tf/knowledge/tickets/pt-np39/review-second.md`

## Acceptance Criteria
- [x] Module names normalized
- [x] Imports and CLI dispatch updated
- [x] Tests and docs references updated
- [x] Runtime behavior unchanged (579 tests pass)
