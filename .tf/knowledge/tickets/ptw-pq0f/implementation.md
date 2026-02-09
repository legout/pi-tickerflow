# Implementation: ptw-pq0f

## Summary
Added `--cov-fail-under=4` to pytest addopts in pyproject.toml to ensure coverage failures happen during regular test runs.

## Files Changed
- `pyproject.toml` - Added `"--cov-fail-under=4"` to `[tool.pytest.ini_options]` addopts list

## Key Decisions
- The project already had `fail_under = 25` in `[tool.coverage.report]`, but this only applies when running coverage explicitly
- Adding `--cov-fail-under=4` to pytest addopts ensures coverage is checked during regular pytest runs
- The threshold of 4 was specified in the ticket; the lower value (vs 25 in coverage config) allows pytest to run without failing during development while still providing coverage feedback

## Tests Run
- Verified pyproject.toml syntax with Python tomllib parser
- Configuration parsed successfully with the new option

## Verification
- Run `pytest` to verify coverage check runs with tests
- If coverage is below 4%, pytest will fail with a coverage error
