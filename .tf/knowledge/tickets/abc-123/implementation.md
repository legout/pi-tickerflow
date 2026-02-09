# Implementation: abc-123

## Summary
Hello-world utility module verified and ready. Package includes CLI support and comprehensive tests.

## Files Changed
- `demo/__init__.py` - Package init, exports `hello`
- `demo/hello.py` - Main greeting function with docstring
- `demo/__main__.py` - CLI entry point
- `tests/test_demo_hello.py` - Unit tests (4 tests)

## Key Decisions
- Used `from __future__ import annotations` for consistency
- CLI handles multi-word names via `" ".join(sys.argv[1:]).strip()`
- Added pytestmark for unit test categorization
- Module docstring includes examples and CLI usage
- Empty/whitespace-only input falls back to "World"

## Tests Run
```bash
python -m pytest tests/test_demo_hello.py -v
# 4 passed in 0.03s
```

## Verification
```bash
python -c "from demo.hello import hello; print(hello()); print(hello('Test'))"
# Hello, World!
# Hello, Test!

python -m demo Alice
# Hello, Alice!
```
