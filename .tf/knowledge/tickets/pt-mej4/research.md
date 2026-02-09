# Research: pt-mej4

## Status
Research enabled. No additional external research was performed - this is a local codebase testing task.

## Context Reviewed

### Current Coverage Status
- Overall coverage: 49.5%
- Current fail_under threshold: 25% (pyproject.toml)
- pytest addopts has: `--cov-fail-under=4` (inconsistent!)

### Modules with 0% Coverage (Targeted in Ticket)
1. **tf_cli/setup.py** (51 statements) - Global setup for Pi extensions
2. **tf_cli/login.py** (79 statements) - API key configuration for MCP/web-search
3. **tf_cli/tags_suggest.py** (74 statements) - Component tag suggestion CLI
4. **tf_cli/seed_cli.py** (101 statements) - Seed session management
5. **tf_cli/agentsmd.py** (259 statements) - AGENTS.md management commands

### Existing Test Patterns
From reviewing existing tests:
- Tests use pytest with unittest-style classes
- Mocking via unittest.mock (patch, MagicMock)
- tmp_path fixture for filesystem operations
- pytest.mark.unit for unit tests

### Implementation Plan
1. Create test files for each 0% coverage module
2. Fix inconsistent coverage thresholds (4% vs 25%)
3. Raise threshold incrementally to ~35% (safe jump from 25%)
4. Verify all tests pass

## Sources
- `tk show pt-mej4`
- `pyproject.toml` coverage configuration
- Existing test files in tests/ directory
