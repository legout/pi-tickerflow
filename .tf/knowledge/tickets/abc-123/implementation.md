# Implementation: abc-123

## Summary
Demo hello-world utility is complete and fully functional. All acceptance criteria met:
- hello() function in demo/hello.py accepts name parameter with default "World"
- Comprehensive docstrings following project conventions
- 11 tests in tests/test_demo_hello.py covering normal and edge cases
- CLI entry point in demo/__main__.py using argparse

## Retry Context
- Attempt: 1 (fresh run - previous attempts were all closed successfully)
- Escalated Models: fixer=base, reviewer-second=base, worker=base

## Files Changed
- `demo/hello.py` - Core greeting function with type validation and whitespace handling
- `demo/__main__.py` - CLI entry point using argparse
- `demo/__init__.py` - Module exports
- `tests/test_demo_hello.py` - Comprehensive test suite (11 tests)

## Key Decisions
- Used argparse for CLI (following project convention from AGENTS.md)
- Added type validation for None and non-string inputs with clear error messages
- Whitespace-only strings fall back to "World" (consistent behavior)
- __all__ exports defined for both demo and demo.hello modules
- Full test coverage including CLI, type errors, and edge cases

## Tests Run
```bash
python -m pytest tests/test_demo_hello.py -v
```
Result: 11 passed in 0.03s

## Verification
- All unit tests pass
- CLI works: python -m demo [name]
- Library import works: from demo.hello import hello
