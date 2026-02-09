# Implementation: ptw-gbod

## Summary
Added and documented optional arguments for `/tf-backlog` to disable automatic behaviors: deps, component tags, and links. The flags were already documented but the flag parsing logic needed to be formalized.

## Files Changed

### 1. `prompts/tf-backlog.md`
- Added **Phase 0: Flag Parsing** section with robust flag parsing logic
- Updated ticket_factory example to respect the flags:
  - `component_tags=not flags['no_component_tags']`
  - `dep_mode = 'none' if flags['no_deps'] else 'chain'`
  - Conditional `apply_links()` based on `flags['no_links']`

### 2. `.pi/agent/skills/tf-planning/SKILL.md`
- Updated **Flags** section to list all four flags with descriptions
- Added **Flag Parsing (Phase 0)** section with code example
- Updated step 2 to reference flag parsing
- Updated ticket_factory example to respect flags

## Key Decisions

1. **Flag parsing is robust**: Unknown flags produce a warning and are ignored (as per ticket constraints)
2. **Defaults remain enabled**: All automatic behaviors are ON by default; flags explicitly disable them
3. **Documentation complete**: Both the prompt and skill file have consistent examples showing flag usage

## Flags Implemented

| Flag | Effect |
|------|--------|
| `--no-deps` | Skip automatic dependency inference |
| `--no-component-tags` | Skip automatic component tag assignment |
| `--no-links` | Skip automatic linking of related tickets |
| `--links-only` | Run only linking on existing backlog tickets |

## Tests Run

- Python flag parsing code validated with test cases
- Unknown flag warning mechanism verified
- All flags properly toggle their respective behaviors

## Verification

To verify the implementation works:

```bash
# Test with all opt-out flags
/tf-backlog seed-myfeature --no-deps --no-component-tags --no-links

# Test links-only mode
/tf-backlog seed-myfeature --links-only

# Test unknown flag warning
/tf-backlog seed-myfeature --unknown-flag  # Should warn and ignore
```
