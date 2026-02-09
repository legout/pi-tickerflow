# Review: pt-ooda

## Overall Assessment
The implementation provides comprehensive test documentation and guided manual testing scripts for the TUI document opening feature. All three reviewers agree the test coverage is thorough and the scripts are well-structured. However, there are concerns about the ticket completion criteria, script robustness, and a potential security issue in the underlying code being tested.

**Reviewers**: reviewer-general, reviewer-spec-audit, reviewer-second-opinion

---

## Critical (must fix)

### 1. Tests Not Actually Executed
- **File**: `test_results.md` (all checkboxes unchecked)
- **Issue**: The ticket acceptance criteria requires actually running and documenting tests (`- [ ] Test with $PAGER=less`, etc.), not just creating test infrastructure. The implementation provides test procedures but does not complete the actual testing work.
- **Why it matters**: Spec defines tasks to complete, not deliverables to create. Testing cannot be meaningfully completed until pt-d9rg (terminal suspend) is implemented.
- **Source**: reviewer-spec-audit

### 2. Test Premise Compromised (Blocked Dependency)
- **File**: Test approach overall
- **Issue**: The research.md correctly identifies `os.system(cmd)` runs WITHOUT `self.app.suspend()`, meaning tests will cause terminal corruption. Testing documentation describing tests that cannot pass is misleading.
- **Recommendation**: Add prominent warning that tests are expected to fail until pt-d9rg is complete, or re-scope ticket to "create test infrastructure" rather than "perform tests".
- **Source**: reviewer-second-opinion

### 3. Command Injection Vulnerability (In Code Under Test)
- **File**: `tf_cli/ui.py` (code being tested, not test script)
- **Issue**: The `_open_doc` method constructs commands like `f'{pager} "{full_path}"'`. Malicious paths with backticks or `$()` could execute arbitrary commands.
- **Note**: This is an issue in the code being tested, not the test script itself. Should be addressed in pt-d9rg or a follow-up security ticket.
- **Source**: reviewer-second-opinion

---

## Major (should fix)

### 4. set -e with read Commands May Cause Unexpected Exits
- **File**: `test_doc_opening.sh:9, 70, 85, 100, 115, 130, 145, 160`
- **Issue**: `set -e` combined with `read -p` may cause abrupt termination if EOF encountered (non-interactive mode) or piped input.
- **Fix**: Add `|| true` to read commands or handle exit case explicitly.
- **Source**: reviewer-general, reviewer-second-opinion

### 5. REPO_ROOT Calculation is Fragile
- **File**: `test_doc_opening.sh:35`
- **Issue**: Uses hardcoded `../../../..` relative to script location. Breaks if directory structure changes or script is copied.
- **Fix**: Use `git rev-parse --show-toplevel` for robust repository root detection.
- **Source**: reviewer-general, reviewer-second-opinion

### 6. Missing Executable Permission Documentation
- **File**: `implementation.md`, `test_doc_opening.sh`
- **Issue**: Implementation notes claim "Scripts Verified" includes executable permission, but no documentation explains how execute bit is set or preserved in git.
- **Fix**: Document git permission handling or add `chmod +x` instruction.
- **Source**: reviewer-second-opinion

---

## Minor (nice to fix)

### 7. Inconsistent Function Naming Convention
- **File**: `test_doc_opening.sh:21-23, 25-27`
- **Issue**: `log_info`/`log_warn`/`log_error` vs `print_header` - mixed naming conventions.
- **Fix**: Use consistent prefix (e.g., `log_header` or `print_info`).
- **Source**: reviewer-general

### 8. find Command Could Be Slow
- **File**: `test_doc_opening.sh:48`
- **Issue**: `find` for sample topics without depth limit could be slow in large knowledge directories.
- **Fix**: Add `-maxdepth 3` for performance.
- **Source**: reviewer-general

### 9. Checkbox Emoji Compatibility
- **File**: `test_results.md:1`
- **Issue**: ⬜ emoji may not render consistently across all markdown viewers.
- **Fix**: Use `[ ]` syntax for better compatibility.
- **Source**: reviewer-general

### 10. No Interactive Pass/Fail Prompts
- **File**: `test_doc_opening.sh:60`
- **Issue**: Script prompts to start test but doesn't capture pass/fail/skip during execution.
- **Fix**: Add interactive prompts for test results.
- **Source**: reviewer-spec-audit

### 11. POSIX Compliance - which vs command -v
- **File**: `test_doc_opening.sh:40-43`
- **Issue**: `which` is non-standard; POSIX prefers `command -v`.
- **Fix**: Use `command -v` for better portability.
- **Source**: reviewer-second-opinion

### 12. Hardcoded ANSI Color Codes
- **File**: `test_doc_opening.sh:9`
- **Issue**: ANSI escapes may not work on Windows or minimalist terminals.
- **Fix**: Consider using `tput` for portable colors.
- **Source**: reviewer-second-opinion

---

## Warnings (follow-up ticket)

### 13. Script Version Tracking
- **File**: `test_doc_opening.sh:3`
- **Issue**: No version number or "last verified" date. If pt-d9rg changes implementation, test script may need updates.
- **Source**: reviewer-general

### 14. CI/CD Integration Gap
- **File**: `test_doc_opening.sh` overall
- **Issue**: Entire test suite is manual/interactive. No automated validation possible.
- **Suggestion**: Create separate automated test using mock pager to verify command construction.
- **Source**: reviewer-general, reviewer-second-opinion

### 15. Missing Tool Pre-flight Check
- **File**: `test_doc_opening.sh`
- **Issue**: Assumes less, more, vim, nano are installed without checking.
- **Suggestion**: Add pre-flight check warning which tools are missing.
- **Source**: reviewer-general

### 16. Test Results Archiving Strategy
- **File**: `test_results.md`
- **Issue**: No guidance on whether results should be committed, moved, or cleaned up.
- **Source**: reviewer-second-opinion

---

## Suggestions (follow-up ticket)

1. **Add --quick/--smoke mode** - Single representative test for rapid validation (reviewer-general)
2. **Time tracking** - Add "Time Taken" field to test_results.md (reviewer-general)
3. **Screenshot guidance** - Document visual capture for TUI restoration issues (reviewer-general)
4. **PAGER=bat test** - Add test for popular modern pager (reviewer-general)
5. **Automated smoke tests** - Verify test script runs without errors non-interactively (reviewer-spec-audit)
6. **Invalid command test** - Document expected behavior for unknown pager/editor (reviewer-spec-audit)
7. **Nested path test** - Test subdirectories in topic folders (reviewer-spec-audit)
8. **Special characters test** - Verify paths with spaces and special chars (reviewer-second-opinion)
9. **Mock unit tests** - Mock os.system to verify command construction (reviewer-second-opinion)
10. **Command logging** - Record actual commands via `set -x` for debugging (reviewer-second-opinion)
11. **verify command** - Check all required tools installed before running (reviewer-second-opinion)

---

## Positive Notes

- **Comprehensive coverage**: All 8 acceptance criteria addressed with clear, actionable procedures (all reviewers)
- **Well-structured script**: Effective function use, color-coded output, supports individual and full suite runs (reviewer-general)
- **User-friendly design**: Specific key sequences reduce ambiguity (e.g., "Type ':q' to exit vim") (reviewer-general, reviewer-second-opinion)
- **Excellent research.md**: Thorough analysis of implementation state and pt-d9rg dependency (reviewer-spec-audit, reviewer-second-opinion)
- **Professional template**: test_results.md structure suitable for QA documentation (reviewer-second-opinion)
- **Error handling**: Prerequisites checked with clear error messages (reviewer-general)

---

## Summary Statistics
- Critical: 3
- Major: 3
- Minor: 6
- Warnings: 4
- Suggestions: 11

## Spec Coverage
- Ticket: `tk show pt-ooda` - ✓ Consulted
- Seed: `.tf/knowledge/topics/seed-fix-tui-doc-opening/seed.md` - ✓ Consulted
- Code: `tf_cli/ui.py` lines 540-610 - ✓ Reviewed
- Missing specs: None identified
