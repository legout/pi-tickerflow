# Research: ptw-gbod

## Status
Research minimal - straightforward implementation task. The documentation already exists in `prompts/tf-backlog.md`, but the flag handling needs verification and potential fixes.

## Context Reviewed
- `prompts/tf-backlog.md` - Already documents `--no-deps`, `--no-component-tags`, `--no-links` flags
- `tf_cli/ticket_factory.py` - Has `component_tags` parameter and `mode="none"` for dependencies
- `tf_cli/backlog_ls_new.py` - Related backlog listing functionality

## Key Findings

1. **Documentation exists**: The prompt file already has:
   - Usage section with flags documented
   - Examples for each flag
   - Detailed explanation in Execution section

2. **Implementation partially exists**:
   - `create_tickets()` has `component_tags: bool = True` parameter
   - `apply_dependencies()` has `mode: str = "chain"` parameter (can use "none")
   - `apply_links()` is a separate call that can be skipped

3. **Gap identified**: The Execution section in the prompt references the flags but the flag parsing and passing to functions may need verification.

## Implementation Plan
1. Verify flag parsing in prompt execution section
2. Ensure flags properly passed to ticket_factory functions
3. Add robust flag parsing (ignore unknown flags with warning as per constraints)
4. Update help/examples if needed

## Sources
- (none - local codebase review only)
