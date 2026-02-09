# Implementation: pt-ynqf

## Summary
Refactored CLI modules to import shared utilities from `tf_cli.utils` instead of using local duplicate definitions.

## Files Changed

### 1. `tf_cli/ralph_new.py`
- **Added**: Import `find_project_root` from `tf_cli.utils`
- **Removed**: Local `find_project_root()` function definition (lines 83-88)
- **Rationale**: The shared utility provides the same functionality with additional support for `.pi` directory detection

### 2. `tf_cli/ticket_factory.py`
- **Added**: Import `find_project_root` from `tf_cli.utils`
- **Changed**: Updated `write_backlog_md()` to use `find_project_root()` instead of `_find_project_root()`
- **Removed**: Local `_find_project_root()` function definition (lines 383-390)
- **Rationale**: Eliminates duplicate code, uses shared implementation

## Key Decisions

1. **Preserved `session_store._read_json()`**: This function has different semantics from `utils.read_json()` - it returns `None` on failure instead of `{}`. Changing this would require updating all callers, which is out of scope for this no-behavior-change pass.

2. **Used absolute imports**: Changed `from .utils import` to `from tf_cli.utils import` for consistency with other imports in these modules.

## Test Results

All 512 tests pass after refactoring:
```
============================= 512 passed in 3.25s ==============================
```

Specific test coverage:
- `tests/test_utils.py` - All utility function tests pass
- `tests/test_ralph_logging.py` - Ralph logging tests pass
- All other existing tests continue to pass

## Verification

Verified module imports work correctly:
```python
from tf_cli.ralph_new import main  # OK
from tf_cli.ticket_factory import create_tickets  # OK
from tf_cli.utils import find_project_root, read_json, merge  # OK
```

## Acceptance Criteria

- [x] Target modules import shared helpers
- [x] Duplicate helper definitions removed
- [x] Full test suite passes unchanged behavior
