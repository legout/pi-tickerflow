# Research: pt-hpme

## Status
Research completed. Existing policy and architecture clear.

## Context Reviewed
- `tk show pt-hpme` - Task to implement tf_cli compatibility shims
- `tk show pt-mu0s` - Deprecation strategy defined (closed)
- `tk show pt-62g6` - Entrypoints wired to use tf namespace (closed)
- `docs/deprecation-policy.md` Section 3.4 - tf_cli → tf deprecation policy

## Key Decisions from pt-mu0s
- Timeline: Support tf_cli through 0.4.x, removal in 0.5.0
- Warnings: Opt-in via TF_CLI_DEPRECATION_WARN=1 (default off to avoid CI noise)
- Documentation: Updated docs/deprecation-policy.md with Section 3.4

## Current State
- `tf/` package exists but imports FROM `tf_cli/` (reversed)
- `tf_cli/` has the canonical implementation
- pyproject.toml entrypoint: `tf = "tf.cli:main"` (correctly points to tf)

## Target State
- `tf/` has canonical implementation
- `tf_cli/` is thin shim re-exporting from `tf/`
- Opt-in deprecation warnings when TF_CLI_DEPRECATION_WARN=1

## Implementation Plan
1. Update `tf/__init__.py` - make it canonical (re-export from tf, not tf_cli)
2. Update `tf/cli.py` - move full CLI dispatcher here from tf_cli/cli.py
3. Update `tf_cli/__init__.py` - shim re-exporting from tf with optional warning
4. Update `tf_cli/cli.py` - shim re-exporting from tf.cli with optional warning
5. Ensure `tf_cli/version.py` and other modules get shim treatment

## Sources
- pt-mu0s notes (commit ff2aee3)
- pt-62g6 notes (commit 574e3de)
- docs/deprecation-policy.md
