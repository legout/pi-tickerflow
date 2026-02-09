# Research: pt-1vz2

## Status
Research enabled. Minimal external research needed - this is a standard repository hygiene task.

## Rationale
- The task involves standard pre-commit/CI guardrails for file size and path restrictions
- Common patterns are well-established in the industry
- Project is Python-based with existing tooling (pytest, ruff implied by pyproject.toml)

## Approach
1. Create a Python guardrails script in `scripts/` (consistent with existing tf_config.py)
2. Install as pre-commit hook via setup script or manual copy
3. Create GitHub Actions workflow for CI enforcement
4. Document behavior in docs/

## Thresholds Decided
- **Max file size**: 5MB (reasonable for code repositories)
- **Forbidden paths**: Common build/runtime artifacts
  - `node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `.pytest_cache/`,
  - `build/`, `dist/`, `*.egg-info/`, `.tox/`, `.coverage`, `htmlcov/`

## Sources
- (none - standard practice)
