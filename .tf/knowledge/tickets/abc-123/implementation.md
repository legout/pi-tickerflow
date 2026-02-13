# Implementation: abc-123

## Summary
Demo hello-world utility for IRF workflow testing. The implementation is complete with all 12 tests passing.

## Retry Context
- Attempt: 1
- Escalated Models: fixer=base, reviewer-second=base, worker=base

## Files Changed
- `demo/hello.py` - Hello-world utility with greeting function
- `demo/__init__.py` - Module exports
- `demo/__main__.py` - CLI entry point
- `tests/test_demo_hello.py` - Comprehensive test suite (12 tests)

## Key Decisions
- Implemented `hello()` function with default parameter "World"
- Added Unicode whitespace handling (zero-width chars U+200B-U+200D, U+FEFF)
- Added type validation with TypeError for non-string inputs
- CLI supports both `python -m demo` and `python -m demo <name>` usage
- Comprehensive test coverage including edge cases

## Tests Run
```bash
$ python -m pytest tests/test_demo_hello.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0 -- /home/volker/.local/bin/python
collected 12 items

tests/test_demo_hello.py::test_hello_default PASSED                      [  8%]
tests/test_demo_hello.py::test_hello_custom_name PASSED                  [ 16%]
tests/test_demo_hello.py::test_hello_empty_string PASSED                 [ 25%]
tests/test_demo_hello.py::test_hello_whitespace_only PASSED              [ 33%]
tests/test_demo_hello.py::test_hello_whitespace_stripped PASSED          [ 41%]
tests/test_demo_hello.py::test_hello_unicode_whitespace_stripped PASSED  [ 50%]
tests/test_demo_hello.py::test_cli_default PASSED                        [ 58%]
tests/test_demo_hello.py::test_cli_with_name PASSED                      [ 66%]
tests/test_demo_hello.py::test_cli_empty_string PASSED                   [ 75%]
tests/test_demo_hello.py::test_hello_none_raises PASSED                  [ 83%]
tests/test_demo_hello.py::test_hello_non_string_raises PASSED            [ 91%]
tests/test_demo_hello.py::test_module_exports PASSED                     [100%]

============================== 12 passed in 0.04s ==============================
```

## Verification
All 12 tests pass. The implementation meets all acceptance criteria:
- ✅ Hello-world utility in `demo/hello.py`
- ✅ Function accepts name parameter with default "World"
- ✅ Includes comprehensive docstring
- ✅ 12 tests covering functionality and edge cases
