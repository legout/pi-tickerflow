# Fixes: ptw-ykvx

## Major Issues Fixed

### Unused Imports (Line 17-19)
**Issue**: `check_extension` and `load_workflow_config` were imported but never used directly in test functions.

**Fix**: Removed the unused imports from the import statement.

```python
# Before:
from tf_cli.doctor import (
    build_parser,
    check_extension,
    load_workflow_config,
    run_doctor,
)

# After:
from tf_cli.doctor import (
    build_parser,
    run_doctor,
)
```

## Minor Issues Fixed

### pytestmark Placement (Line 15)
**Issue**: The module-level `pytestmark` was placed before local imports, which is unconventional.

**Fix**: Moved `pytestmark` after all imports for better readability.

```python
# Before:
import pytest

pytestmark = pytest.mark.integration

from tf_cli.doctor import (...)

# After:
from tf_cli.doctor import (...)

import pytest

pytestmark = pytest.mark.integration
```

### Unused Fixture Return Values (Lines 69-75)
**Issue**: The `mock_dependencies` fixture yielded a dictionary of mock objects that were never used by test functions.

**Fix**: Simplified the fixture to not yield values since the patches are applied as side effects.

```python
# Before:
@pytest.fixture
def mock_dependencies(self):
    with (
        mock.patch("shutil.which", return_value="/usr/bin/tk"),
        mock.patch("tf_cli.doctor.check_cmd") as mock_check_cmd,
        ...
    ):
        yield {
            "check_cmd": mock_check_cmd,
            "check_ext": mock_check_ext,
            "check_mcp": mock_check_mcp,
        }

# After:
@pytest.fixture
def mock_dependencies(self):
    with (
        mock.patch("shutil.which", return_value="/usr/bin/tk"),
        mock.patch("tf_cli.doctor.check_cmd"),
        ...
    ):
        yield
```

## Warnings Not Fixed (Follow-up Ticket Candidates)

1. **Git dependency without graceful skip** - Would require restructuring the test with try/except
2. **Documentation inconsistency** - Minor typo in implementation.md
3. **Overly permissive e2e test** - Would require conditional test logic

## Verification

All 14 tests pass after fixes:
```
14 passed in 1.61s
```
