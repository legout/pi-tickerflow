# Implementation: pt-e7hj

## Summary
Define and document the runtime artifact policy for .tf/.tickets/generated outputs, clarifying what is source-controlled vs runtime/generated state.

## Files Changed

### 1. `docs/artifact-policy.md` (NEW)
Created comprehensive policy document covering:
- Quick reference table for all artifact categories
- Detailed rules for `.tf/knowledge/` (mixed content)
- Detailed rules for `.tf/ralph/` (mixed content)
- Rules for `.tickets/`, build artifacts, and runtime files
- Contributor guidelines for deciding what to commit
- Common mistakes to avoid

### 2. `.gitignore` (MODIFIED)
Expanded from 3 lines to comprehensive 42-line ignore file:
- Added `.tf/knowledge/tickets/` (runtime ticket artifacts)
- Added Python build artifacts (`*.egg-info/`, `build/`, `dist/`)
- Added virtual environment patterns (`.venv/`, `env/`, `venv/`)
- Added testing artifacts (`.pytest_cache/`, `.tox/`)
- Added Node.js patterns (`node_modules/`)
- Added IDE/editor patterns (`.vscode/`, `.idea/`)
- Added OS patterns (`.DS_Store`, `Thumbs.db`)
- Added header comment linking to policy doc

### 3. `README.md` (MODIFIED)
Added link to new artifact policy in Documentation section:
- `- **[docs/artifact-policy.md](docs/artifact-policy.md)** - Source-controlled vs runtime artifacts`

## Key Decisions

1. **Mixed content approach for `.tf/knowledge/`**: Topics (plans, seeds, spikes) are source-controlled because they represent durable project knowledge. Ticket artifacts (reviews, implementations) are runtime because they can be regenerated.

2. **Comprehensive .gitignore**: Rather than minimal ignores, we provide a complete template that covers common Python/Node development patterns plus TF-specific artifacts.

3. **Contributor-focused policy**: The document emphasizes practical guidance ("Ask yourself...") over abstract rules to help contributors make correct decisions.

## Verification

```bash
# Policy document exists and is readable
cat docs/artifact-policy.md | head -20

# .gitignore includes key patterns
grep -E "(tickets/|egg-info|venv)" .gitignore

# README links to policy
grep "artifact-policy" README.md
```

## Acceptance Criteria Status

- [x] Policy doc created and linked from README/docs
- [x] Explicit rules for .tf/knowledge, .tf/ralph/sessions, .tickets, htmlcov, *.egg-info
- [x] Contributor guidance for local-only state

## Related

- Plan: plan-critical-cleanup-simplification
- Blocks: pt-mr22 (CLN-02: Expand .gitignore for Python/build/runtime artifact noise)
