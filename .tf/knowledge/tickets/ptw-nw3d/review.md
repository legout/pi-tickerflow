# Review: ptw-nw3d

## Critical (must fix)
- `tf_cli/version.py:89` - Module-level `__version__ = get_version()` evaluates at import time and caches the result. If the VERSION file is not found during import (e.g., in a containerized environment), "unknown" will be permanently cached even if VERSION becomes available later. Tests that mock `get_version()` after import won't affect the cached `__version__` value. (Source: reviewer-general)

## Major (should fix)
- `tf_cli/version.py:82-85` - The CWD fallback checks for VERSION in the current working directory, which can return incorrect version when running `tf` from a different project directory that has its own VERSION file. Consider removing this fallback or making it opt-in. (Source: reviewer-general)
- `README.md` - Versioning scheme (SemVer) is defined in seed.md but not documented in user-facing docs. The seed requires "Adopt SemVer (MAJOR.MINOR.PATCH) and document how to bump versions," but there's no documentation explaining version bumping procedures. (Source: reviewer-spec-audit)
- `tests/test_version.py:51` - The test `test_falls_back_to_module_parent` lacks an assertion statement. After calling `version.get_version()`, the test should assert `result == "2.0.0"` to verify the fallback behavior actually works. (Source: reviewer-second-opinion)

## Minor (nice to fix)
- `tf_cli/_version.py:4` - The deprecation notice is only in the docstring. Consider adding a runtime deprecation warning using `warnings.warn(DeprecationWarning, stacklevel=2)`. (Source: reviewer-general)
- `tf_cli/version.py:66` - The fallback order includes VERSION in current working directory as an edge case. While documented, this is unusual and could cause confusion. (Source: reviewer-spec-audit)
- `tf_cli/version.py:95` - The module-level constant `__version__ = get_version()` is evaluated at import time. If VERSION file doesn't exist at import, `__version__` will be permanently set to "unknown". Consider using a cached function or property instead. (Source: reviewer-second-opinion)
- `tf_cli/version.py:68` - The comment says "VERSION file relative to this module" but the code does `Path(__file__).resolve().parent.parent`, which is two directories up. The comment should clarify it looks in the package root. (Source: reviewer-second-opinion)
- `tf_cli/version.py:78-80` - The working directory fallback checks `cwd / "VERSION"`, which could return a VERSION file from any project. Consider restricting this to only return if from a valid ticketflow project. (Source: reviewer-second-opinion)
- `tf_cli/version.py:42-49` - The `_read_version_file()` function accepts any file content without validation. Consider adding basic validation (e.g., regex pattern like `^\d+\.\d+\.\d+.*`). (Source: reviewer-general)

## Warnings (follow-up ticket)
- `tf_cli/version.py:71-76` - The fallback logic uses `Path(__file__).resolve().parent.parent` which assumes a specific package structure. If the structure changes, this will break. Consider using `importlib.resources` for more robust resolution. (Source: reviewer-general)
- `pyproject.toml:7,12` - No automation for keeping pyproject.toml metadata in sync with VERSION during releases. Related to backlog item ptw-5wmr. (Source: reviewer-spec-audit)
- No documentation exists for how VERSION file should be updated during releases. (Source: reviewer-spec-audit)

## Suggestions (follow-up ticket)
- Consider making `get_version()` cache-aware with a `force_reload` parameter for testing. (Source: reviewer-general)
- The fallback chain could benefit from logging/debug output to help diagnose version detection issues. (Source: reviewer-general)
- Consider adding a `tf doctor version` subcommand that tests all fallback paths. (Source: reviewer-general)
- Consider adding a `tf version bump <major|minor|patch>` helper as mentioned in seed.md. (Source: reviewer-spec-audit)
- Add CHANGELOG.md (seed requirement, separate backlog item ptw-c4ei). (Source: reviewer-spec-audit)
- Consider adding version format validation to ensure returned version matches SemVer format. (Source: reviewer-second-opinion)
- Consider adding integration tests for actual pip and uvx installation scenarios. (Source: reviewer-second-opinion)
- The working directory fallback could be replaced with environment-based detection (e.g., `TF_VERSION`). (Source: reviewer-second-opinion)

## Summary Statistics
- Critical: 1
- Major: 3
- Minor: 8
- Warnings: 3
- Suggestions: 8
