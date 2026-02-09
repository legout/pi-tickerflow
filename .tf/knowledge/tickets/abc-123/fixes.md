# Fixes: abc-123

## Fixed Issues

### Critical (1 fixed)
- `pyproject.toml:62` - Added `"demo"` to coverage `source` list so the demo package is included in coverage tracking.

### Major (1 fixed)
- `demo/__main__.py` - Refactored CLI to use `argparse` instead of raw `sys.argv` parsing:
  - Changed `main()` signature to accept `argv: Optional[list[str]] = None`
  - Added `argparse.ArgumentParser` with proper help text
  - Added positional `name` argument with default "World"
  - Updated docstring with examples showing multi-word name support
  - Now follows project convention established in `tf/hello.py`

## Verification
```bash
python -m demo
# Hello, World!

python -m demo Alice
# Hello, Alice!

python -m demo --help
# usage: demo [-h] [name]
# Print a hello message
```

All 4 tests passing after fixes.
