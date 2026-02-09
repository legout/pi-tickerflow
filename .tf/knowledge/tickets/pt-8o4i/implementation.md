# Implementation: pt-8o4i

## Summary
Updated `tf_cli/login.py` to write a command-based `zai-vision` MCP server configuration instead of the legacy URL-based endpoint.

## Files Changed
- `tf_cli/login.py` - Modified `configure_mcp()` function

## Key Changes

### Before (URL-based):
```python
set_server("zai-vision", "https://api.z.ai/api/mcp/vision/mcp", headers=headers, auth="bearer")
```

### After (Command-based):
```python
# zai-vision uses command-based server
mcp_config["mcpServers"]["zai-vision"] = {
    "command": "npx",
    "args": ["-y", "@z_ai/mcp-server"],
    "env": {"Z_AI_API_KEY": zai_key, "Z_AI_MODE": "ZAI"}
}
```

## Verification

### Tests Run
```bash
python -m pytest tests/test_login.py -v
```
Result: **17 passed**

### Generated Config Verification
Verified that `zai-vision` now outputs:
```json
{
  "command": "npx",
  "args": ["-y", "@z_ai/mcp-server"],
  "env": {
    "Z_AI_API_KEY": "<key>",
    "Z_AI_MODE": "ZAI"
  }
}
```

While `zai-web-search` and `zai-web-reader` remain URL-based with bearer Authorization headers as required.

## Acceptance Criteria
- [x] `configure_mcp()` writes `zai-vision` with: `command: npx`, `args: ["-y","@z_ai/mcp-server"]`, and `env: {Z_AI_API_KEY, Z_AI_MODE="ZAI"}`
- [x] `zai-web-search` and `zai-web-reader` remain URL-based with bearer `Authorization` header
- [x] Generated `mcp.json` remains valid JSON
- [x] File permissions are still best-effort `0o600`

## Constraints Met
- Only `zai-vision` was changed; other servers remain unchanged
- No breaking changes to existing functionality
