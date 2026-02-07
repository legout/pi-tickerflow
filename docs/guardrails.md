# Repository Guardrails

This document describes the repository guardrails that prevent committing oversized files and forbidden runtime/build paths.

## Overview

Guardrails are automated checks that run:
1. **Locally** - As a pre-commit hook before each commit
2. **In CI** - As part of the GitHub Actions workflow

## Checks Performed

### 1. File Size Check

Files larger than **5MB** are blocked from being committed.

**Rationale:** Large files bloat the repository, slow down clones, and are often binary artifacts that should not be version-controlled.

**What to do if you need to commit a large file:**
- Consider using [Git LFS](https://git-lfs.github.com/) for large binary files
- If the file must be committed, discuss with the team and bypass with `git commit --no-verify`

### 2. Forbidden Paths Check

The following paths are blocked from being committed:

| Pattern | Description |
|---------|-------------|
| `.venv/`, `venv/`, `env/` | Python virtual environments |
| `__pycache__/` | Python bytecode cache |
| `.pytest_cache/`, `.mypy_cache/`, `.tox/` | Testing/tooling cache |
| `*.egg-info/`, `.eggs/` | Python package build artifacts |
| `build/`, `dist/` | Build output directories |
| `target/` | Rust build artifacts |
| `node_modules/` | Node.js dependencies |
| `.next/`, `.nuxt/` | Framework build output |
| `.coverage`, `htmlcov/` | Coverage reports |
| `.idea/`, `.vscode/` | IDE configurations (personal) |
| `.DS_Store`, `Thumbs.db` | OS metadata files |
| `*.log` | Log files |

**Rationale:** These are generated files or local environment artifacts that should not be shared. They can be rebuilt or reinstalled from dependency files.

## Installation

### Automatic Installation

Run the install script:

```bash
./scripts/install-guardrails.sh
```

This will install the pre-commit hook in `.git/hooks/pre-commit`.

### Manual Installation

Create `.git/hooks/pre-commit` with:

```bash
#!/bin/bash
python3 scripts/guardrails.py --staged-only
```

## Usage

### Check All Files

```bash
python3 scripts/guardrails.py
```

### Check Only Staged Files (like pre-commit)

```bash
python3 scripts/guardrails.py --staged-only
```

### Custom Size Limit

```bash
python3 scripts/guardrails.py --max-size-mb 10
```

### Quiet Mode (only output on failure)

```bash
python3 scripts/guardrails.py --quiet
```

### Bypass Guardrails (Emergency Only)

```bash
git commit --no-verify
```

⚠️ **Warning:** Only use `--no-verify` in exceptional circumstances and after team discussion.

## CI Integration

Guardrails run automatically in GitHub Actions on every push and pull request. The CI will fail if any guardrails check fails.

See `.github/workflows/ci.yml` for the workflow configuration.

## Configuration

Currently, thresholds and patterns are defined in `scripts/guardrails.py`:

- `DEFAULT_MAX_SIZE_MB` - Maximum file size in megabytes
- `DEFAULT_FORBIDDEN_PATTERNS` - List of regex patterns for forbidden paths

To modify these, edit the script and commit the changes.

## Troubleshooting

### "Guardrails script not found"

Ensure you're running from the repository root:

```bash
cd $(git rev-parse --show-toplevel)
```

### Pre-commit hook not running

Check that the hook is executable:

```bash
ls -la .git/hooks/pre-commit
```

If needed, make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Adding exceptions

If you need to add an exception (e.g., a large fixture file that must be committed):

1. Discuss with the team
2. Consider if the file belongs in the repo or should be downloaded/generated
3. If necessary, bypass with `--no-verify` and document the exception

## Future Improvements

Potential enhancements to consider:

- [ ] Support for custom configuration file (e.g., `.guardrails.yml`)
- [ ] Allowlist for specific files that exceed limits
- [ ] Integration with pre-commit framework
- [ ] Configurable per-project thresholds
