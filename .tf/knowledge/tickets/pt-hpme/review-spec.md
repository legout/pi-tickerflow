# Review (Spec Audit): pt-hpme

## Overall Assessment

The implementation successfully meets the core acceptance criteria for ticket pt-hpme. The tf_cli compatibility shims are implemented as thin re-exports with opt-in deprecation warnings matching the defined strategy from pt-mu0s. The shims avoid warning spam in default test runs and preserve backward compatibility. However, there is one major gap: the verification section mentions smoke tests that do not actually exist in the test suite.

## Critical (must fix)

None

## Major (should fix)

- `tf_cli/__init__.py:6-19` - Missing smoke test for shim compatibility. The implementation verification section in implementation.md claims tests exist ("# Test tf_cli shim works: python -m tf_cli --version"), but `tests/test_smoke_version.py` only tests `tf --version`, not `python -m tf_cli --version` or `import tf_cli`. This is a documentation/spec mismatch that should be addressed either by adding the smoke test or updating the implementation.md to reflect that testing is deferred to pt-m06z (which is explicitly tasked with "add at least one test that imports tf_cli (shim) successfully").
- `implementation.md:62-70` - Verification claims tests that don't exist. The verification section shows test commands for tf_cli shim behavior but these are not automated tests in the test suite. This creates a false sense of coverage. Since pt-m06z (blocked on pt-hpme and pt-tupn) is explicitly tasked with adding shim tests, the implementation.md should clarify this gap.

## Minor (nice to fix)

- `tf_cli/__init__.py:3-6` - The module docstring is verbose with deprecation notice. While accurate, the deprecation message is repeated in the code comments, warnings, and docstring. This is minor but could be consolidated for readability.
- `tf_cli/cli.py:6-19` - Inconsistent warning message format. The warning says "tf_cli.cli is deprecated" but the message text doesn't include the removal version (0.5.0) like the tf_cli/__init__.py warning does. Minor inconsistency.

## Warnings (follow-up ticket)

- `tf_cli/__init__.py:35-42` - Ticket factory exports are accessed directly from tf_cli during transition. The implementation correctly documents this as temporary ("In pt-tupn, the implementation will move to tf/"), but ensure pt-tupn includes these exports in tf/__init__.py to avoid breaking existing code that imports from `tf_cli.ticket_factory`.
- `tf/cli.py:177-234` - Command handlers imported from tf_cli modules will need to be moved to tf/ in pt-tupn. The implementation correctly notes this in the migration path, but ensure the move maintains all command routing functionality.

## Suggestions (follow-up ticket)

- Consider adding a test in pt-m06z that verifies the can_import_tf_cli alias works correctly for any downstream code using that specific import.
- Consider adding a test that verifies no deprecation warnings are emitted by default (TF_CLI_DEPRECATION_WARN unset) to prevent regression of the "avoid warning spam" constraint.

## Positive Notes

- The opt-in deprecation warning via `TF_CLI_DEPRECATION_WARN=1` environment variable correctly implements the strategy defined in pt-mu0s.
- The shims are correctly implemented as thin re-exports with no duplicated logic.
- Backward compatibility is well maintained: `import tf_cli` works, `python -m tf_cli` works, and the `can_import_tf_cli` alias is preserved.
- Circular import avoidance is handled correctly with `tf/__init__.py` not importing from tf_cli.
- The pyproject.toml entrypoint `tf = "tf.cli:main"` is correctly configured (from pt-62g6).
- Module execution works for both `python -m tf` (pt-ce2e) and `python -m tf_cli` (pt-hpme).
- Documentation in docs/deprecation-policy.md Section 3.4 correctly documents the deprecation strategy.

## Summary Statistics

- Critical: 0
- Major: 2
- Minor: 2
- Warnings: 2
- Suggestions: 2

## Spec Coverage

- Spec/plan sources consulted:
  - Ticket pt-hpme (requirements and acceptance criteria)
  - Plan: plan-refactor-tf-cli-to-tf (phase 4: compatibility shim requirements, overall acceptance criteria)
  - Ticket pt-mu0s (deprecation strategy: timeline, opt-in warnings via TF_CLI_DEPRECATION_WARN)
  - Ticket pt-62g6 (packaging/entrypoints configuration)
  - Ticket pt-ce2e (tf package skeleton)
  - Ticket pt-m06z (test requirements, blocked on pt-hpme and pt-tupn)
  - docs/deprecation-policy.md Section 3.4 (documented deprecation policy)
- Missing specs: none
