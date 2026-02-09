# Fixes: pt-qayw

## Major Fix

### Fixed `extract_ticket_title()` to return `None` on failure (enables graceful omission)

**Issue**: The function returned the ticket ID as fallback when title extraction failed, causing redundant `ticket_title` fields in logs that duplicated the `ticket` field.

**Fix**: Changed `extract_ticket_title()` to return `Optional[str]`:
- Returns the ticket title string when successfully extracted
- Returns `None` when:
  - `tk` command is not available
  - `tk show` fails (non-zero exit)
  - No title line (`# Title`) is found

**Files changed**:
- `tf_cli/ralph.py`: Updated `extract_ticket_title()` function

**Before**:
```python
def extract_ticket_title(ticket: str) -> str:
    if shutil.which("tk") is None:
        return ticket  # Returns ID as fallback
    # ...
    return ticket  # Returns ID as fallback
```

**After**:
```python
def extract_ticket_title(ticket: str) -> Optional[str]:
    """Extract the ticket title from the ticket file.

    Returns:
        The ticket title if found, None otherwise (enables graceful omission in logs)
    """
    if shutil.which("tk") is None:
        return None
    # ...
    return title if title else None
```

**Impact**: The `ticket_title` field is now truly optional in logs. When `extract_ticket_title()` returns `None`, the logger's `if ticket_title:` check fails and the field is gracefully omitted from output.

## Verification

All 79 tests in test_logger.py and test_ralph_logging.py pass.
