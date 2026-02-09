# Implementation: pt-cje7

## Summary
Added documentation note about the new `zai-vision` MCP server type, clarifying its local npx-based execution model and prerequisites.

## Files Changed
- `docs/configuration.md` - Added note to MCP servers table clarifying:
  - `zai-vision` runs locally via `npx -y @z_ai/mcp-server`
  - Requires Node.js with npx available
  - `zai-web-search` and `zai-web-reader` remain remote URL-based services
- `CHANGELOG.md` - Added entry under [Unreleased] documenting the change

## Key Decisions
- Placed the note directly in the MCP servers table for visibility
- Used a blockquote note format to distinguish it from regular table content
- Updated CHANGELOG to track the documentation change for the next release

## Tests Run
- N/A (documentation-only change)

## Verification
- Review `docs/configuration.md` section "Available MCP Servers" to confirm the note is present
- Review `CHANGELOG.md` under [Unreleased] > Added to confirm entry exists
