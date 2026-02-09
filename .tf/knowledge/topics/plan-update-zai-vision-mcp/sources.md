# Sources

## Prompt

- User request: Analyze current `~/.pi/agent/mcp.json` and compare with `tf setup` generated version
- Focus: Difference in zai-vision MCP server configuration

## Files Analyzed

- `~/.pi/agent/mcp.json` - Current working configuration (command-based zai-vision)
- `tf_cli/login.py` - Source of generated configuration (URL-based zai-vision)
- `tests/test_login.py` - Tests that verify MCP configuration

## Key Differences Found

### Current Config (Working)
- `zai-vision`: command-based using `npx -y @z_ai/mcp-server`
- Environment variables: `Z_AI_API_KEY`, `Z_AI_MODE`

### Generated Config (Legacy)
- `zai-vision`: URL-based pointing to `https://api.z.ai/api/mcp/vision/mcp`
- Bearer auth via `Authorization` header

## References

- MCP Server Type documentation: command-based vs URL-based
- ZAI MCP npm package: `@z_ai/mcp-server`
