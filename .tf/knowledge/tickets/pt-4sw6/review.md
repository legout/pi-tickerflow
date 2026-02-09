# Review: pt-4sw6

## Critical (must fix)

- `tests/test_backlog_session_aware.py:8-13` - Remove unused imports (`json`, `Mock`, `patch` from `unittest.mock`) to maintain code cleanliness

- `tests/test_backlog_session_aware.py:42-52` - `test_no_arg_uses_root_seed_when_session_active` only verifies `load_active_session()` returns a session with `root_seed`. It does NOT test actual Phase A.2 behavior: "Use the session's `root_seed` as the topic". Test should verify topic resolution logic, not just session data existence.

## Major (should fix)

- `tests/test_backlog_session_aware.py:90-95` - `test_explicit_topic_overrides_session_default` is tautological. Assigns `explicit_topic` to `resolved_topic` then asserts they match, without testing actual override logic. Documents intent but doesn't verify production behavior.

- `tests/test_backlog_session_aware.py:77-83` - `test_no_arg_without_session_requires_explicit_topic` lacks assertion of failure behavior. Only asserts `active_session is None` but doesn't test that topic resolution fails or requires explicit input as docstring claims.

- `tests/test_backlog_session_aware.py:282-296` - `test_notice_includes_all_inputs_used` validates manually constructed string matching spec format, but doesn't test actual `/tf-backlog` command emits this notice during execution.

- `tests/test_backlog_session_aware.py:377-393` - `test_only_active_session_used_for_default` has convoluted logic working around `load_active_session` returning content regardless of state. Consider clarifying what layer is responsible for state filtering.

- Missing test coverage: No tests verify `backlog.inputs_used` object schema from spec step 11 (Session Finalization), which requires: `seed`, `plan`, `plan_status`, `spikes`, `spikes_read`, `spikes_missing`.

## Minor (nice to fix)

- `tests/test_backlog_session_aware.py:131-136` - `test_explicit_topic_same_as_root_seed_uses_explicit` uses helper `create_seed_with_session` but doesn't actually test "uses explicit path" behavior - just verifies session exists. Could be more comprehensive.

- `tests/test_backlog_session_aware.py:266-276` - Helper `create_seed_with_session` is only used in one test. Consider inlining it or using consistently across tests that create sessions.

- `tests/test_backlog_session_aware.py:279-328` - `build_ticket_context` helper extracts content using string operations (`find()`, slicing) which is fragile. Consider proper frontmatter parser (acceptable for test code but worth noting).

- `tests/test_backlog_session_aware.py:21-22` - Import of `Generator` from `typing` only used for fixture type hint. Could be removed if type checking relaxed for tests.

- `tests/test_backlog_session_aware.py:236-237` - `test_build_ticket_context_missing_docs_warns` adds non-existent spike but doesn't verify warning is emitted to user, only that `check_missing_docs` returns it. Notification coverage incomplete.

## Warnings (follow-up ticket)

- `tests/test_backlog_session_aware.py:1-433` - Tests simulate Phase B incorporation logic via helpers (`build_ticket_context`, `check_missing_docs`), but don't test actual production code. Follow-up ticket should add integration tests verifying real `/tf-backlog` command behavior.

- `tests/test_backlog_session_aware.py:1` - No tests for malformed session data (missing `root_seed`, wrong schema version, corrupted JSON). Production code handles these but backlog tests don't verify.

- `tests/test_backlog_session_aware.py:1` - No tests for when session-linked artifacts exist but are empty or have malformed frontmatter. `build_ticket_context` helper extracts by string matching which could fail silently.

- `tests/test_backlog_session_aware.py:400-412` - `test_session_preserved_when_explicit_topic_provided` doesn't actually test preservation behavior - just asserts session exists before and after. Without triggering explicit topic code path that might modify session, test has limited value.

## Suggestions (follow-up ticket)

- Consider adding tests for edge cases: malformed session data, corrupted plan.md/spike.md files, very long seed/plan/spike IDs, special characters in IDs

- Add test for session state transitions during backlog operation (should session be modified when backlog is generated?)

- Consider property-based testing for input resolution to catch edge cases in topic/seed/plan/spike ID combinations

- The notification tests (lines 350-412) test string formatting but don't verify actual logging/output capture. Consider using `caplog` fixture to verify actual log output.

- Consider adding tests for edge cases from spec Phase B.3: "If plan/spike docs are missing or unreadable: emit warning, continue with seed-only"

- Consider adding tests for plan status checking from spec Phase B.1: "Warn if plan status is not `approved`"

- Consider adding `resolve_topic_for_backlog()` function to `session_store` module that formalizes topic resolution logic currently only tested via direct attribute access

## Positive Notes

- ✅ Excellent test organization into 5 clear test classes covering different aspects
- ✅ Good use of existing `temp_kb_dir` fixture pattern from `test_session_store.py` for consistency
- ✅ Tests correctly avoid external dependencies - no real `tk` calls, no network access
- ✅ `temp_topics_dir` fixture creates realistic document structures with proper frontmatter
- ✅ All 18 tests pass and complete quickly (0.11s), indicating good test isolation
- ✅ Type hints used consistently throughout
- ✅ Helper functions well-documented with docstrings explaining purpose as test utilities
- ✅ All 3 acceptance criteria from ticket are addressed at input-resolution layer

## Summary Statistics
- Critical: 2
- Major: 5
- Minor: 5
- Warnings: 4
- Suggestions: 7
