---
id: plan-update-zai-vision-mcp
status: draft
last_updated: 2026-02-09
---

# Plan: Update `tf setup` to use new ZAI Vision MCP server

## Summary

Update the `configure_mcp` function in `tf_cli/login.py` to generate the new **command-based** ZAI Vision MCP server configuration instead of the legacy **URL-based** configuration.

The new approach runs `@z_ai/mcp-server` locally via npx, which provides better performance and access to ZAI's vision capabilities through a local MCP server rather than a remote HTTP endpoint.

## Current State vs Desired State

### Current `~/.pi/agent/mcp.json` (working configuration)
```json
"zai-vision": {
  "command": "npx",
  "args": ["-y", "@z_ai/mcp-server"],
  "env": {
    "Z_AI_API_KEY": "<key>",
    "Z_AI_MODE": "ZAI"
  }
}
```

### What `tf setup` currently generates (legacy)
```json
"zai-vision": {
  "url": "https://api.z.ai/api/mcp/vision/mcp",
  "auth": "bearer",
  "headers": {
    "Authorization": "Bearer <key>"
  }
}
```

## Requirements

- [ ] Update `configure_mcp()` in `tf_cli/login.py` to generate command-based ZAI Vision config
- [ ] Keep zai-web-search and zai-web-reader as URL-based (they remain remote APIs)
- [ ] Only zai-vision should use the command-based approach
- [ ] Preserve existing API key handling (read from input or ZAI_API_KEY env var)
- [ ] Ensure the generated mcp.json maintains proper permissions (0o600)
- [ ] Test that the new configuration works with Pi's MCP client

## Changes Needed

### File: `tf_cli/login.py`

The `configure_mcp` function needs a new helper to add command-based servers:

```python
def set_command_server(name: str, command: str, args: list[str], env: dict[str, str]):
    srv = {"command": command, "args": args, "env": env}
    mcp_config["mcpServers"][name] = srv
```

Then modify the zai-vision configuration:

**Current code:**
```python
set_server("zai-vision", "https://api.z.ai/api/mcp/vision/mcp", headers=headers, auth="bearer")
```

**New code:**
```python
set_command_server(
    "zai-vision",
    "npx",
    ["-y", "@z_ai/mcp-server"],
    {"Z_AI_API_KEY": zai_key, "Z_AI_MODE": "ZAI"}
)
```

## Acceptance Criteria

- [ ] Running `tf setup` (or `tf login`) generates mcp.json with command-based zai-vision
- [ ] The generated config matches the working configuration structure exactly
- [ ] zai-web-search and zai-web-reader remain unchanged (URL-based)
- [ ] All other MCP servers (context7, exa, grep_app) remain unchanged
- [ ] Existing tests pass or are updated appropriately

## Testing Plan

1. Run `tf login` with a test ZAI API key
2. Verify `~/.pi/agent/mcp.json` contains the command-based zai-vision entry
3. Verify the MCP server starts correctly via Pi's MCP client
4. Verify zai-web-search and zai-web-reader still work as URL-based servers

## Test Updates Required

The test `test_includes_zai_servers_with_key` in `tests/test_login.py` currently asserts URL-based config. It needs updating:

**Current assertion:**
```python
assert "zai-vision" in config["mcpServers"]
headers = config["mcpServers"]["zai-web-search"]["headers"]
assert headers["Authorization"] == "Bearer zai-key"
```

**New assertions needed:**
```python
# zai-web-search and zai-web-reader remain URL-based
assert "zai-web-search" in config["mcpServers"]
assert config["mcpServers"]["zai-web-search"]["url"].startswith("https://")
assert config["mcpServers"]["zai-web-search"]["headers"]["Authorization"] == "Bearer zai-key"

# zai-vision is now command-based
assert "zai-vision" in config["mcpServers"]
assert config["mcpServers"]["zai-vision"]["command"] == "npx"
assert config["mcpServers"]["zai-vision"]["args"] == ["-y", "@z_ai/mcp-server"]
assert config["mcpServers"]["zai-vision"]["env"]["Z_AI_API_KEY"] == "zai-key"
assert config["mcpServers"]["zai-vision"]["env"]["Z_AI_MODE"] == "ZAI"
```

## Related Files

- `tf_cli/login.py` - Main file to modify
- `tests/test_login.py` - Test updates required

## References

- Working config location: `~/.pi/agent/mcp.json`
- ZAI MCP server package: `@z_ai/mcp-server`
