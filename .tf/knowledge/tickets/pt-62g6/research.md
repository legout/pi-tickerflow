# Research: pt-62g6

## Status
Research completed. No external research needed - this is an internal refactoring task.

## Context Reviewed

### Current State
- `pyproject.toml` has entrypoint: `tf = "tf_cli.cli:main"`
- `tf_cli` package exists with `cli.py` containing `main()` function
- `tf_cli/__main__.py` delegates to `cli.main()`
- Tests exist in `tests/test_smoke_version.py` for `tf --version`

### Required Changes
Per ticket requirements:
1. Create new `tf` package as the canonical implementation location
2. Wire entrypoints to use `tf` namespace instead of `tf_cli`
3. Keep `tf_cli` working (compatibility shims) for backward compatibility
4. Add smoke test for console script

### Implementation Approach
1. Create `tf/` directory with minimal structure:
   - `tf/__init__.py` - package marker
   - `tf/cli.py` - imports and re-exports from `tf_cli.cli`
2. Update `pyproject.toml`:
   - Change `[project.scripts]` entrypoint to `tf = "tf.cli:main"`
   - Add `"tf"` to `[tool.setuptools.packages]`
3. The smoke test `test_smoke_version.py` already tests `tf --version`

## Sources
- `pyproject.toml` - current entrypoint configuration
- `tf_cli/cli.py` - main CLI implementation
- `tf_cli/__main__.py` - module execution entrypoint
- `tests/test_smoke_version.py` - existing smoke tests
