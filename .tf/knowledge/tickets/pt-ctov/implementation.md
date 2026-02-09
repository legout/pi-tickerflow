# Implementation: pt-ctov

## Summary
Documented the P0–P4 priority rubric and `/tf-priority-reclassify` command in README and docs/commands.md. Updated the prompt help text to match implementation options.

## Files Changed

### 1. `README.md`
- Added **Priority Rubric (P0–P4)** section with:
  - Priority mapping table (P0-P4 with descriptions)
  - Classification examples table
  - Priority reclassification command documentation
  - Command options table
- Added `/tf-priority-reclassify` to Commands Overview table

### 2. `docs/commands.md`
- Added **Priority Reclassification Commands** section with:
  - Full command usage and arguments
  - P0–P4 rubric table
  - Classification keywords table
  - Multiple usage examples
  - Notes on customizing classification rules

### 3. `prompts/tf-priority-reclassify.md`
- Updated Arguments table to include all implementation flags:
  - `--yes` - Skip confirmation
  - `--max-changes N` - Safety cap
  - `--force` - Apply ambiguous classifications
  - `--include-closed` - Include closed tickets
  - `--include-unknown` - Show unknown priorities
  - `--json` - JSON output
  - `--report` - Write audit trail

## Key Decisions

1. **Documentation placement**: Added the rubric as a top-level section in README (between Knowledge Base and Configuration) so it's easily discoverable.

2. **Command naming**: Used `/tf-priority-reclassify` in README commands table for consistency with other Pi commands, while noting the CLI entry point is `tf new priority-reclassify`.

3. **Rubric detail level**: Included the full rubric table in README for quick reference, with more detailed keyword classifications in docs/commands.md.

4. **Customization notes**: Added instructions in docs/commands.md for extending classification rules by editing `RUBRIC`, `TAG_MAP`, and `TYPE_DEFAULTS` in the Python source.

## Verification

- README renders correctly with new rubric section
- Commands table includes priority-reclassify
- docs/commands.md includes complete command reference
- Prompt help text matches implementation options

## Tests Run

```bash
# Verify Python CLI help matches documentation
python -m tf_cli new priority-reclassify --help

# Verify ticket still shows correctly
tk show pt-ctov
```
