# Implementation: pt-fsk3

## Summary
Implemented shared helper functions for kb commands in `tf_cli/kb_helpers.py`:
- `resolve_knowledge_dir` - Resolve knowledgeDir from config with CLI override support
- `atomic_read_index` - Atomically read and parse index.json
- `atomic_write_index` - Atomically write index.json using tmp+rename

## Files Changed
- `tf_cli/kb_helpers.py` (new) - Helper functions for kb commands
- `tf_cli/kb_cli.py` (modified) - Updated to use new helpers
- `tests/test_kb_helpers.py` (new) - Unit tests for all helper functions

## Key Decisions
- Kept all code stdlib-only as per constraints
- Used tempfile.mkstemp + os.replace for atomic writes
- Resolution priority: CLI override > env var > config file > default
- Refactored kb_cli.py to import from kb_helpers instead of duplicating code

## Tests Run
```bash
$ python -m pytest tests/test_kb_helpers.py -v
23 passed

$ python -m pytest tests/ -v
271 passed
```

## Verification
All tests pass including new unit tests covering:
- CLI override priority
- Environment variable resolution
- Config file parsing (absolute and relative paths)
- Default fallback behavior
- Atomic read operations
- Atomic write operations
- Error handling (corrupted JSON, permission errors)
