# Review (Spec Audit): pt-4sw6

## Overall Assessment
The implementation adds 18 unit tests covering session-aware topic resolution and input incorporation for `/tf-backlog`. The tests meet the ticket's constraint of not calling real tk or requiring network access. However, the tests primarily validate helper functions that simulate spec behavior rather than testing actual implementation code paths.

## Critical (must fix)
- `tests/test_backlog_session_aware.py:42-52` - `test_no_arg_uses_root_seed_when_session_active` only verifies that `load_active_session()` returns a session object with a `root_seed` field. It does NOT test the actual Phase A.2 behavior from the spec: "If no argument provided and session is active: Use the session's `root_seed` as the topic". The test should verify the topic resolution logic, not just session data existence.
- `tests/test_backlog_session_aware.py:171-179` - `build_ticket_context()` is a test helper function that duplicates spec logic rather than testing production code. Per the spec Phase B.1-B.4, the actual implementation should read from `.tf/knowledge/topics/{plan}/plan.md` and `.tf/knowledge/topics/{spike}/spike.md`. The tests validate helper behavior, not actual file reading/incorporation logic.

## Major (should fix)
- `tests/test_backlog_session_aware.py:282-296` - `test_notice_includes_all_inputs_used` validates a manually constructed string that matches the spec format `[tf] Inputs: seed={topic-id} plan={plan-id|none} spikes={count} [...]`, but does not test that the actual `/tf-backlog` command emits this notice during execution. The spec (prompts/tf-backlog.md Output section) requires this as actual output behavior.
- `tests/test_backlog_session_aware.py:77-93` - `test_explicit_topic_overrides_session_default` sets a local variable `explicit_topic` and asserts it differs from `root_seed`, but does not test actual argument parsing or the resolution logic from spec Phase A.2: "If explicit topic argument provided: Use it (bypass session default)".
- `tests/test_backlog_session_aware.py:54-62` - `test_no_arg_without_session_requires_explicit_topic` is incomplete - it only asserts no session exists but does not test the "Fall back to auto-locate" behavior from spec Phase A.2 or verify any error/prompt behavior.
- Missing test coverage: No tests verify the `backlog.inputs_used` object schema from spec step 11 (Session Finalization), which requires specific fields: `seed`, `plan`, `plan_status`, `spikes`, `spikes_read`, `spikes_missing`.

## Minor (nice to fix)
- `tests/test_backlog_session_aware.py:301-311` - `test_notice_shows_none_for_missing_plan` tests notice formatting but uses hardcoded string construction rather than testing actual output generation code.
- `tests/test_backlog_session_aware.py:335-349` - `test_only_active_session_used_for_default` has confusing logic - it sets state to archived then checks if state != active to set `can_use_as_default = False`. This test would benefit from clearer assertions about the expected behavior when session state is not "active".

## Warnings (follow-up ticket)
- `tests/test_backlog_session_aware.py:1-433` - The test file tests helper functions (`build_ticket_context`, `check_missing_docs`) rather than actual production code. If the production implementation of `/tf-backlog` diverges from these helpers, the tests will pass while the feature is broken. Recommend a follow-up ticket to add integration tests that verify actual command behavior with mocked file system.

## Suggestions (follow-up ticket)
- Consider adding tests for edge cases from spec Phase B.3: "If plan/spike docs are missing or unreadable: emit warning, continue with seed-only". Current `test_build_ticket_context_missing_docs_warns` only tests the `check_missing_docs` helper, not actual warning emission.
- Consider adding tests for plan status checking from spec Phase B.1: "Warn if plan status is not `approved`".

## Positive Notes
- ✅ Tests follow the constraint of not calling real tk or requiring network access
- ✅ Uses existing session_store API and fixtures pattern from test_session_store.py for consistency  
- ✅ All 3 acceptance criteria from ticket are addressed at the input-resolution layer
- ✅ Tests cover topic resolution (4 tests), session inputs (4 tests), input incorporation (4 tests), notifications (4 tests), and state validation (2 tests)
- ✅ `temp_topics_dir` fixture creates realistic seed/plan/spike document structures for testing

## Summary Statistics
- Critical: 2
- Major: 5
- Minor: 2
- Warnings: 1
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted: 
  - `.tf/knowledge/tickets/pt-gmpy/implementation.md` (parent ticket spec)
  - `prompts/tf-backlog.md` (current prompt spec with Phase A and Phase B)
  - `tests/test_backlog_session_aware.py` (implementation under review)
- Missing specs: None - all relevant specs were located and consulted
