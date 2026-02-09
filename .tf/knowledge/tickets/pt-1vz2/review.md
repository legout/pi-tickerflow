# Review: pt-1vz2

Merged review from reviewer-general, reviewer-spec-audit, and reviewer-second-opinion.

## Critical (must fix)

- `scripts/guardrails.py:45-48` - Unanchored patterns `venv(/|$)`, `env(/|$)` will match unintended paths like `myvenv/`, `development/`, `environment/`. These should be anchored like `^venv(/|$)` to only match virtual environment directories at the repo root. (from reviewer-general, reviewer-second-opinion)
- `scripts/guardrails.py:47` - Pattern `\.env(/|$)` matches `.env` directories but will also match `.environment/` or `.envfile.txt`. Should use `^\.env(/|$)` for safety. (from reviewer-general, reviewer-second-opinion)
- `docs/guardrails.md:37,54` - Documentation error: Manual installation instructions reference `cp scripts/pre-commit .git/hooks/pre-commit` but this file doesn't exist; only `scripts/install-guardrails.sh` is provided. Users following these instructions will get "No such file or directory" error. (from reviewer-spec-audit, reviewer-second-opinion)

## Major (should fix)

- `scripts/guardrails.py:58,75` - `subprocess` imported inside functions rather than at module level. This is inconsistent and causes re-import overhead on each call. Move to top-level imports. (from reviewer-general, reviewer-second-opinion)
- `scripts/guardrails.py:37` - Pattern `\.egg-info(/|$)` not anchored, could match `myproject.egg-info/` within a valid directory. (from reviewer-general)
- `scripts/guardrails.py:88-96` - When paths are provided as arguments, the code uses `os.walk()` which doesn't respect `.gitignore`. This could cause false positives. (from reviewer-second-opinion)
- `scripts/guardrails.py:122` - Regex patterns use `re.search()` which matches anywhere. Patterns should consistently use `^` anchors to avoid partial path matching. (from reviewer-second-opinion)

## Minor (nice to fix)

- `scripts/guardrails.py:98` - `check_file_size` returns `True, 0` on OS/IO errors, silently ignoring failures. Should at least log a warning. (from reviewer-general)
- `scripts/guardrails.py:155` - Files that don't exist are silently skipped with `continue`. In staged-only mode, this could mask issues where a staged file was deleted. (from reviewer-general)
- `scripts/install-guardrails.sh:34` - The generated hook doesn't validate that `python3` exists, which could cause confusing errors. (from reviewer-general)
- `.github/workflows/ci.yml:14` - Hardcoded Python 3.11 while test matrix uses 3.9-3.12. Consider consistency or using `3.x`. (from reviewer-general)
- `scripts/guardrails.py:13-14` - Hardcoded configuration. A config file would make this more maintainable. (from reviewer-second-opinion)
- `docs/guardrails.md:98` - Missing Windows instructions. Windows developers need to know how to run the Python script directly. (from reviewer-second-opinion)
- `scripts/install-guardrails.sh:8` - No validation that we're in a git repo before continuing. (from reviewer-second-opinion)
- `scripts/guardrails.py:30` - Missing common patterns: `.ruff_cache/`, `.uv/` which are increasingly common. (from reviewer-second-opinion)

## Warnings (follow-up ticket)

- `scripts/guardrails.py` - No unit tests for the guardrails script. Functions like `check_file_size`, `check_forbidden_path`, `format_size` should have test coverage. (from all reviewers)
- `scripts/guardrails.py:106` - Symlinks not handled: `os.path.getsize()` follows symlinks and reports target file size. A symlink to a large file outside the repo would incorrectly flag as oversized. (from reviewer-second-opinion)
- `scripts/guardrails.py:113` - Binary files not detected with special handling. Consider adding binary file detection with helpful messaging about Git LFS. (from reviewer-second-opinion)
- `.github/workflows/ci.yml` - CI workflow doesn't cache pip dependencies for test/lint jobs, causing slower builds. (from reviewer-general)
- No way to configure exceptions per-project (e.g., legitimate large fixture file). An allowlist would be more flexible. (from reviewer-general)

## Suggestions (follow-up ticket)

- Consider integrating with the pre-commit framework (`pre-commit` package) for better cross-platform support. (from reviewer-general, reviewer-second-opinion)
- Add a `--fix` or `--suggest` mode that outputs `.gitignore` entries for detected forbidden paths. (from reviewer-general, reviewer-second-opinion)
- Consider adding a progress indicator for large repositories with many files. (from reviewer-general)
- Consider adding support for a `.guardrails.yml` config file for per-project customization. (from reviewer-spec-audit)
- Support allowlist for legitimate large files (e.g., `# guardrails: allow-large-file` comment). (from reviewer-second-opinion)

## Positive Notes

- Clean separation of concerns between the main script, installer, CI workflow, and documentation
- All three acceptance criteria are correctly implemented
- Good use of `git ls-files` to respect `.gitignore` in the default mode
- Installer properly backs up existing pre-commit hooks before overwriting
- Pre-commit hook gracefully handles missing guardrails script
- Exit codes correctly used (0 for success, 1 for failure) following Unix conventions
- Human-readable file size formatting is a nice UX touch
- CI workflow runs guardrails as a separate fast-failing job
- Comprehensive documentation with troubleshooting section

## Summary Statistics
- Critical: 3
- Major: 5
- Minor: 8
- Warnings: 5
- Suggestions: 5
