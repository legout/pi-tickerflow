# Research: pt-8o4i

## Status
Research complete. No external research needed - ticket is straightforward internal change.

## Task Summary
Update `tf_cli/login.py` to write a command-based `zai-vision` MCP server config instead of URL-based.

## Current Implementation
In `configure_mcp()` function:
```python
set_server("zai-vision", "https://api.z.ai/api/mcp/vision/mcp", headers=headers, auth="bearer")
```

## Required Changes
Change `zai-vision` from URL-based to command-based:
```python
mcp_config["mcpServers"]["zai-vision"] = {
    "command": "npx",
    "args": ["-y", "@z_ai/mcp-server"],
    "env": {"Z_AI_API_KEY": zai_key, "Z_AI_MODE": "ZAI"}
}
```

## Constraints
- Only change `zai-vision` server
- Keep `zai-web-search` and `zai-web-reader` as URL-based with bearer Authorization header
- Maintain 0o600 file permissions
- Keep valid JSON output

## Files to Modify
- `tf_cli/login.py` - Update `configure_mcp()` function

## Test Impact
- `tests/test_login.py` - Test `test_includes_zai_servers_with_key` checks `zai-vision` exists
  - This test only checks for existence, not structure, so should still pass
  - But the test assertions for headers on `zai-vision` specifically will need updating

## Sources
- `tk show pt-8o4i`
- `tf_cli/login.py` source code
- `tests/test_login.py` test cases
