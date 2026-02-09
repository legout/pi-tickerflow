# Implementation: pt-1vz2

## Summary
Implemented repository guardrails to prevent committing oversized files and forbidden runtime/build paths. The solution includes:

1. **Guardrails script** (`scripts/guardrails.py`) - Main checking logic
2. **Pre-commit hook installer** (`scripts/install-guardrails.sh`) - Easy setup
3. **GitHub Actions workflow** (`.github/workflows/ci.yml`) - CI enforcement
4. **Documentation** (`docs/guardrails.md`) - Usage and configuration guide

## Files Changed

### New Files
- `scripts/guardrails.py` (6841 bytes) - Main guardrails checking script
- `scripts/install-guardrails.sh` (1655 bytes) - Hook installer script
- `.github/workflows/ci.yml` (1501 bytes) - CI workflow with guardrails job
- `docs/guardrails.md` (4019 bytes) - Documentation
- `.git/hooks/pre-commit` (auto-generated) - Pre-commit hook

### Modified Files
- None

## Key Decisions

### Thresholds
- **Max file size**: 5MB (reasonable for code repos, catches accidental binary commits)
- **Forbidden patterns**: 26 regex patterns covering common build/runtime artifacts

### Implementation Approach
- Python script for portability and ease of maintenance
- Uses `git ls-files` to respect .gitignore
- Supports both full-repo and staged-files-only modes
- Exit codes: 0 = pass, 1 = fail (standard for hooks)

### CI Integration
- Added as first job in CI workflow (fast failure)
- Runs on Ubuntu with Python 3.11
- Separate from test/lint jobs for clear error reporting

## Tests Run

```bash
# Full repository check
$ python3 scripts/guardrails.py
============================================================
REPOSITORY GUARDRAILS CHECK
============================================================

✅ All checks passed (193 files checked)
   - Max file size: 5MB
   - Forbidden patterns: 26
```

```bash
# Pre-commit hook installation
$ ./scripts/install-guardrails.sh
✅ Guardrails pre-commit hook installed successfully!
```

## Verification

1. **Manual check**: Run `python3 scripts/guardrails.py`
2. **Pre-commit hook**: Automatically runs on `git commit`
3. **CI check**: Runs on every PR/push via GitHub Actions
4. **Bypass**: `git commit --no-verify` (emergency only)

## Acceptance Criteria Status

- [x] Check fails for oversized files above agreed threshold (5MB)
- [x] Check fails for forbidden runtime/build paths (26 patterns)
- [x] Guardrail behavior documented (docs/guardrails.md)

## Notes

- The pre-commit hook is installed locally and not committed to the repo
- Each developer must run `./scripts/install-guardrails.sh` to enable locally
- The CI will catch violations regardless of local hook installation
