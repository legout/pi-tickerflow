# Implementation: pt-7sv0

## Summary
Created a shared CLI utility module (`tf_cli/utils.py`) and refactored five CLI modules to eliminate code duplication for `find_project_root()`, `read_json()`, and `merge()` functions.

## Files Changed

### New Files
- `tf_cli/utils.py` - New shared utility module containing:
  - `read_json(path)` - Read and parse JSON file with graceful error handling
  - `find_project_root(start)` - Find project root by looking for .tf/.pi directories
  - `merge(a, b)` - Deep merge two dictionaries

- `tests/test_utils.py` - Comprehensive test suite for the utility module (17 tests)

### Modified Files
1. `tf_cli/sync_new.py`
   - Removed duplicate `read_json()` and `find_project_root()` functions
   - Added import: `from .utils import find_project_root, read_json`

2. `tf_cli/doctor_new.py`
   - Removed duplicate `read_json()`, `merge()`, and `find_project_root()` functions
   - Added import: `from .utils import find_project_root, merge, read_json`

3. `tf_cli/backlog_ls_new.py`
   - Removed duplicate `read_json()` and `find_project_root()` functions
   - Added import: `from .utils import find_project_root, read_json`

4. `tf_cli/next_new.py`
   - Removed duplicate `find_project_root()` function
   - Added import: `from .utils import find_project_root`

5. `tf_cli/priority_reclassify_new.py`
   - Removed duplicate `find_project_root()` function
   - Added import: `from .utils import find_project_root`

6. `scripts/tf_config.py`
   - Removed duplicate `read_json()` and `merge()` functions
   - Added import path manipulation and: `from tf_cli.utils import merge, read_json`

7. `.tf/scripts/tf_config.py`
   - Same changes as scripts/tf_config.py (kept in sync)

## Key Decisions

1. **Unified find_project_root behavior**: The shared implementation checks for both `.tf` and `.pi` directories, which is the most permissive of all previous implementations. This maintains backward compatibility while being more flexible.

2. **Preserved function signatures**: All functions maintain their original signatures to ensure backward compatibility with existing code.

3. **Type annotations**: Added proper type annotations in the shared module for better IDE support and documentation.

4. **Comprehensive tests**: Created 17 unit tests covering all edge cases including:
   - Valid and invalid JSON parsing
   - Missing file handling
   - Unicode content support
   - Project root discovery with .tf/.pi markers
   - Deep merge functionality with nested dictionaries
   - Immutability of input dictionaries

## Tests Run

```bash
# New utility module tests
python -m pytest tests/test_utils.py -v
# Result: 17 passed

# Existing tests for refactored modules
python -m pytest tests/test_sync_new.py tests/test_next_new.py -v
# Result: 33 passed

# Full test suite (excluding heavy tests)
python -m pytest tests/ -v --ignore=tests/test_doctor_version.py ...
# Result: 156 passed
```

## Verification

All modules import correctly:
- `tf_cli.utils` imports OK
- `tf_cli.sync_new` imports OK
- `tf_cli.doctor_new` imports OK
- `tf_cli.backlog_ls_new` imports OK
- `tf_cli.next_new` imports OK
- `tf_cli.priority_reclassify_new` imports OK
- `scripts.tf_config` imports OK

## Acceptance Criteria

- [x] Common module created with tests
- [x] Root resolution and JSON helper centralized
- [x] Existing behavior preserved (all 156 tests pass)
