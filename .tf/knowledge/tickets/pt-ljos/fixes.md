# Fixes: pt-ljos

## Critical Fixes

### 1. Security: Unsanitized command in structured log fields
**File**: `tf_cli/logger.py`
**Issue**: The `extra["command"]` was set to raw command before sanitization, exposing secrets in structured logs.
**Fix**: Moved sanitization before building extra dict, so `extra["command"]` now contains sanitized command.

### 2. TypeError: Unexpected keyword argument 'iteration'
**File**: `tf_cli/logger.py`
**Issue**: `log_error_summary()` didn't accept `iteration` parameter but callers passed it.
**Fix**: Added `iteration: Optional[int] = None` parameter to `log_error_summary()` method.

## Major Fixes

### 3. Incomplete command sanitization patterns
**File**: `tf_cli/logger.py`
**Issue**: Patterns only handled space-separated flags (`--api-key value`), not equals-separated (`--api-key=value`).
**Fix**: Added patterns for equals-separated formats:
- `r'(--api-key[=:]\S+)'` → `'--api-key=[REDACTED]'`
- `r'(--token[=:]\S+)'` → `'--token=[REDACTED]'`
- `r'(--secret[=:]\S+)'` → `'--secret=[REDACTED]'`
- `r'(--password[=:]\S+)'` → `'--password=[REDACTED]'`

### 4. Incomplete JWT pattern
**File**: `tf_cli/logger.py`
**Issue**: Pattern `(eyJ[\w-]*\.eyJ[\w-]*)` only captured header.payload (2 parts).
**Fix**: Changed to `(eyJ[\w-]*\.eyJ[\w-]*\.[\w-]*)` to capture all 3 JWT parts (header.payload.signature).

## Minor Fixes

### 5. Consistent event naming
**File**: `tf_cli/logger.py`
**Issue**: `log_no_ticket_selected()` used `event="no_ticket"` which was inconsistent with method name.
**Fix**: Changed to `event="no_ticket_selected"` for consistency.

### 6. Added iteration support to log_no_ticket_selected
**File**: `tf_cli/logger.py`, `tf_cli/ralph_new.py`
**Issue**: `log_no_ticket_selected()` didn't accept iteration parameter for consistency with other methods.
**Fix**: Added `iteration: Optional[int] = None` parameter and updated callers in ralph_new.py to pass iteration.

## Files Changed

- `tf_cli/logger.py` - Fixed sanitization, added iteration support, improved patterns
- `tf_cli/ralph_new.py` - Updated calls to pass iteration to log_no_ticket_selected()

## Verification

All fixes verified with Python tests:
- log_error_summary with iteration parameter
- log_no_ticket_selected with iteration and event name
- Command sanitization with equals format (--key=value)
- JWT 3-part sanitization
- log_command_executed structured field sanitization
