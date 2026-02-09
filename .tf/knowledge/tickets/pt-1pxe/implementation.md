# Implementation: pt-1pxe

## Summary
Implemented `tf kb ls` and `tf kb show` commands for the knowledge base management CLI.

## Files Changed
- `tf_cli/kb_cli.py` - Complete rewrite of kb CLI with ls/show/index commands
- `tf_cli/kb_helpers.py` - Added new helper functions for topic management
- `tests/test_kb_helpers.py` - Updated tests for topics structure and added new tests

## Key Decisions
1. **Topic structure**: Used `topics` array from index.json (not `entries`) to match actual data structure
2. **Topic type derivation**: Type is derived from ID prefix (seed-, plan-, spike-, baseline-)
3. **Archive handling**: Topics are considered archived if they exist in `.tf/knowledge/archive/topics/`
4. **Document tracking**: Show command displays which doc files exist with checkmarks

## Acceptance Criteria
- [x] `ls` lists active topics from index.json with basic fields
- [x] `ls --type seed|plan|spike|baseline` filters by id prefix
- [x] `ls --archived` includes archived topics by scanning archive directory
- [x] `show` prints topic metadata and key doc paths and indicates archived status

## Tests Run
```bash
# Basic listing
python -m tf_cli.cli kb ls
# Shows 7 active topics with type and title

# Filter by type
python -m tf_cli.cli kb ls --type seed
# Shows 4 seed topics

# Show specific topic
python -m tf_cli.cli kb show seed-kb-management-commands
# Shows metadata, keywords, and document existence

# JSON output
python -m tf_cli.cli kb ls --json
python -m tf_cli.cli kb show plan-kb-management-cli --json

# All kb_helpers tests pass (33 tests)
pytest tests/test_kb_helpers.py -v
```

## Verification
Run these commands to verify the implementation:
```bash
cd /home/volker/coding/pi-ticketflow
python -m tf_cli.cli kb ls
python -m tf_cli.cli kb ls --type plan
python -m tf_cli.cli kb show seed-kb-management-commands
```
