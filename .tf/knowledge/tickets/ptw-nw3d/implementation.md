# Implementation: ptw-nw3d

## Summary
Add a version retrieval helper (`tf_cli/version.py`) that returns the current Ticketflow version reliably across all install modes.

## Files Changed
- `tf_cli/version.py` - New module with `get_version()` function
- `tf_cli/_version.py` - Backward compatibility module
- `tf_cli/cli.py` - Already uses `from tf_cli.version import get_version` and handles `--version` flag
- `VERSION` - Version file containing "0.1.0"

## Key Decisions
- **Single source of truth**: VERSION file at repo root
- **Fallback order**: 
  1. VERSION in resolved repo root (for git checkouts)
  2. VERSION relative to module (for pip/uvx installs)  
  3. VERSION in current working directory (edge case)
  4. "unknown" (final fallback)
- **Repo root detection**: Uses `.tf` directory marker + VERSION file existence, or `pyproject.toml` + `tf_cli` directory
- **Backward compatibility**: `_version.py` provides compatibility shim

## Tests Run
- Verified `get_version()` returns "0.1.0":
  ```python
  from tf_cli.version import get_version
  print(get_version())  # Output: 0.1.0
  ```
- CLI `--version` flag verified in code at `cli.py:418-420`

## Verification
- Import works: `from tf_cli.version import get_version`
- Returns correct version: "0.1.0"
- CLI supports: `tf --version`, `tf -v`, `tf -V`
- Works for git checkout, pip install, and uvx install modes
