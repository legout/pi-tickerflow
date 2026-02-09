# Review: pt-et1v

## Overall Assessment
The implementation is a well-structured audit that confirms `textual serve` works correctly with the Ticketflow UI. The test script validates both knowledge directory resolution and static asset loading. No code changes were required since the inline CSS approach is inherently robust for web serving.

## Critical (must fix)
No issues found - the audit correctly identified that no code changes were necessary.

## Major (should fix)
- `test_textual_serve.py:21-22` - Hard-coded venv path `"/home/volker/coding/pi-ticketflow/.venv/bin/textual"` is fragile and will fail on other machines. Should use `shutil.which("textual")` to find the executable in PATH, with an environment variable override if needed.
- `test_textual_serve.py:28` - Fixed 3-second sleep is unreliable; slow systems may need more time, fast systems waste time. Should poll the server endpoint in a loop with a timeout instead.

## Minor (nice to fix)
- `test_textual_serve.py:95-99` - The CSS loading warning is logged but not treated as a failure, yet the function continues. Consider whether this should affect the return value.
- `ui.py:94-95` - In `open_topic_doc()`, `doc_path` is computed but never used; only `full_path` is actually used. The unused variable should be removed.
- `ui.py:88-102` - The `os.system()` calls for opening documents could potentially have issues with shell escaping if paths contain special characters. Consider using `subprocess.run()` with a list of arguments instead.

## Warnings (follow-up ticket)
- `test_textual_serve.py:52` - The test modifies `sys.path` directly which can have side effects. Consider using `PYTHONPATH` environment variable or running in a subprocess to isolate the test.
- `ui.py:131` - The `_find_repo_root()` function checks for `AGENTS.md` which may not exist in all repository configurations. Consider making the detection criteria more flexible or configurable.

## Suggestions (follow-up ticket)
- Consider adding a proper integration test that runs `textual serve` as a subprocess and uses an HTTP client library like `httpx` or `requests` instead of `urllib.request` for better ergonomics and async support.
- Add a health check endpoint or use Textual's built-in health check mechanism to verify the server is ready before running assertions, instead of the fixed sleep.
- Document the `TF_KNOWLEDGE_DIR` environment variable in the project README so users know they can override the knowledge directory location.

## Positive Notes
- The audit correctly identified that inline CSS makes the app robust for web serving - no external file path issues.
- The `resolve_knowledge_dir()` function has excellent fallback logic (env var → config → repo root → cwd) that handles various deployment scenarios.
- The test script has proper cleanup with terminate/wait/kill sequence to avoid zombie processes.
- The implementation correctly notes that Textual serve provides its own static assets (xterm.css, textual.js) which work out of the box.

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 3
- Warnings: 2
- Suggestions: 3
