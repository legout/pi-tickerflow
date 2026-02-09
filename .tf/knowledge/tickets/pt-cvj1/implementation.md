# Implementation: pt-cvj1

## Summary
Updated unit test `test_includes_zai_servers_with_key` in `tests/test_login.py` to reflect that `zai-vision` is now command-based while `zai-web-search` and `zai-web-reader` remain URL-based.

## Files Changed
- `tests/test_login.py` - Updated `test_includes_zai_servers_with_key` test assertions:
  - Now asserts `zai-web-search` and `zai-web-reader` still have `url` property with https:// prefix and `Authorization: Bearer ...` header
  - Now asserts `zai-vision` uses `command/args/env` structure as specified in the plan
  - Removed the old generic assertion that didn't distinguish between URL-based and command-based servers

## Key Decisions
- Kept assertions specific per acceptance criteria (avoiding brittle full-file comparisons)
- Verified all three ZAI servers are present in config
- Added specific checks for each server type's expected structure

## Tests Run
```bash
pytest tests/test_login.py::TestConfigureMcp::test_includes_zai_servers_with_key -v
# PASSED

pytest tests/test_login.py -v
# All 17 tests PASSED
```

## Verification
The implementation correctly validates:
1. `zai-web-search`: URL-based with Bearer auth header
2. `zai-web-reader`: URL-based with Bearer auth header  
3. `zai-vision`: Command-based with npx, args `[-y, @z_ai/mcp-server]`, and env vars `Z_AI_API_KEY` and `Z_AI_MODE`

This aligns with the actual implementation in `tf_cli/login.py` which was updated in a previous ticket (pt-8o4i).
