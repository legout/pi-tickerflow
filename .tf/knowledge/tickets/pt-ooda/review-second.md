# Review (Second Opinion): pt-ooda

## Overall Assessment
The implementation provides thorough test documentation and a guided manual testing approach for the TUI document opening feature. While the first review covered code quality and style issues well, this second opinion identifies security concerns, structural issues, and dependency problems that could affect the validity of the testing effort.

## Critical (must fix)
- `test_doc_opening.sh:35` - Command injection vulnerability: The `cmd` construction uses double quotes around `$full_path` but passes through shell evaluation. A malicious document path with backticks or `$()` could execute arbitrary commands. The implementation should use `subprocess.run()` with a list of arguments instead of string interpolation, or at minimum use single quotes and proper escaping.
- `test_doc_opening.sh` - The entire test premise is compromised: The research.md correctly identifies that `os.system(cmd)` is called WITHOUT `self.app.suspend()`, meaning these tests will cause terminal corruption when run. Testing documentation that describes tests which cannot possibly pass is misleading. The ticket should either be blocked on pt-d9rg or include a prominent warning that tests are expected to fail.

## Major (should fix)
- `test_doc_opening.sh:35` - `REPO_ROOT` calculation uses hardcoded `../../../..` relative to script location. If the knowledge directory structure changes or the script is copied elsewhere, this breaks. Use `git rev-parse --show-toplevel` instead.
- `test_doc_opening.sh` - Missing executable permission documentation: The implementation notes say "Scripts Verified" includes executable permission, but there's no mention of how the script gets its execute bit set. If this is committed to git without proper permissions, users will get "Permission denied" errors.
- `test_results.md` - No failure impact assessment: When tests fail (which they will without pt-d9rg), there's no guidance on severity or whether the feature can still be released. Add a section explaining which failures are blockers vs acceptable.

## Minor (nice to fix)
- `test_doc_opening.sh:9` - `set -e` with `read -p` can cause abrupt termination if stdin is not a TTY (e.g., piped input). Consider `|| true` or explicit TTY check.
- `test_doc_opening.sh:25-27` - Color codes use hardcoded ANSI escapes rather than `tput`, which may not work on all terminals (e.g., Windows, some minimalist terminals).
- `test_doc_opening.sh:40-43` - The `which` command is non-standard (POSIX prefers `command -v`). This may fail on some Unix variants.
- `implementation.md` - Line references to `tf_cli/ui.py` are approximate ("~lines 540-610"). Use exact line numbers or git permalinks for precision.
- `test_doc_opening.sh` - Script location in `.tf/knowledge/tickets/pt-ooda/` is unusual for executable test scripts. Knowledge directories typically store data, not executables. Consider a `tests/manual/` or `scripts/` directory.

## Warnings (follow-up ticket)
- `test_doc_opening.sh` - The test script requires interactive TUI operation which cannot be automated in CI. Consider adding a `--dry-run` mode that validates command construction without executing.
- `test_results.md` - No archiving strategy: Test results will accumulate in the knowledge directory. Document whether these should be committed, moved to a reports directory, or cleaned up after a release.
- `research.md` - References a blocking ticket pt-d9rg but doesn't include a link or commit reference. If pt-d9rg implementation changes, this research becomes stale.

## Suggestions (follow-up ticket)
- Add a test case for document paths containing spaces and special characters to verify the quoting issues are properly handled.
- Consider creating an automated unit test that mocks `os.system` to verify the correct command is constructed for each environment variable combination.
- The test script could record the actual commands executed (via `set -x` logging) for debugging failed tests.
- Add a `verify` command that checks if all required pagers/editors are installed before running the full test suite.

## Positive Notes
- The research.md provides excellent context about the current implementation state and the blocking dependency on pt-d9rg.
- Test coverage is comprehensive with all acceptance criteria addressed.
- The guided approach with specific key sequences (e.g., "Type ':q' to exit vim") reduces ambiguity for testers.
- Color-coded output in the test script improves user experience.
- The template structure in test_results.md is professional and QA-ready.

## Summary Statistics
- Critical: 2
- Major: 3
- Minor: 5
- Warnings: 3
- Suggestions: 4
