# Implementation: pt-4dji

## Summary
Updated `tf ralph --help` text and documentation to reflect the new default session location (`~/.pi/agent/sessions`) and all override mechanisms.

## Files Changed

### 1. tf_cli/ralph.py
- **What**: Updated `usage()` function help text
- **Changes**:
  - Added "Session Storage" section documenting:
    - Default Pi session directory: `~/.pi/agent/sessions/`
    - Config override via `.tf/ralph/config.json` (`sessionDir` key)
    - Legacy behavior warning and how to handle it
    - `RALPH_FORCE_LEGACY_SESSIONS` environment variable usage

### 2. docs/ralph.md
- **What**: Updated Ralph documentation
- **Changes**:
  - Changed `sessionDir` default from `.tf/ralph/sessions` to `~/.pi/agent/sessions` in config example
  - Updated configuration table to reflect new default
  - Added new "Session Storage" subsection under Configuration explaining:
    - Default location
    - How to configure override
    - Legacy behavior and backward compatibility

### 3. docs/configuration.md
- **What**: Updated main configuration documentation
- **Changes**:
  - Added `sessionDir` setting to Ralph configuration table
  - Added `sessionPerTicket` setting to table
  - Added "Session Storage Notes" section documenting:
    - Default location
    - Legacy location and backward compatibility
    - `RALPH_FORCE_LEGACY_SESSIONS` environment variable
    - Warning behavior when legacy directory detected

## Key Decisions

1. **Precise wording**: Used "Pi's standard session directory" rather than guessing platform-specific paths
2. **Complete coverage**: Documented both config file and environment variable override mechanisms
3. **Legacy mention**: Clearly explained the legacy detection warning behavior
4. **Consistent across docs**: All three files now have consistent information

## Tests Run

- Verified syntax of edited Python file: `python -m py_compile tf_cli/ralph.py`
- Verified markdown files are well-formed

## Verification

1. Run `tf ralph --help` to see updated session storage documentation
2. Check docs/ralph.md for updated configuration section
3. Check docs/configuration.md for Ralph session configuration notes
