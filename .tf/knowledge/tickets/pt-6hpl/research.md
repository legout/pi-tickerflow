# Research: pt-6hpl - Setup datastar-py dependency

## Status
Research complete. Version compatibility confirmed.

## Findings

### datastar-py Version
- **Latest version**: 0.8.0 (as of 2026-02-09)
- **Available versions**: 0.8.0, 0.7.0, 0.6.5, 0.6.4, 0.6.3, 0.6.2, 0.6.1, 0.6.0, 0.5.0, 0.4.4...

### Datastar JS Compatibility
- Ticketflow currently pins Datastar JS to `v1.0.0-RC.7`
- The official datastar-py PyPI page shows examples using `v1.0.0-RC.7` in the CDN URL:
  ```html
  <script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-RC.7/bundles/datastar.js"></script>
  ```
- This confirms datastar-py 0.8.0 is compatible with Datastar JS v1.0.0-RC.7

### What datastar-py Provides
- Server-Sent Event (SSE) generation helpers
- Framework-specific response classes (including Sanic)
- Signal reading helpers
- Attribute generation helpers for data-* attributes

### Sanic Integration
- Import: `from datastar_py.sanic import DatastarResponse, datastar_response`
- Use `DatastarResponse([events])` for multi-target updates
- Use `datastar_respond(request)` for streaming responses

## Decision
Pin to **datastar-py>=0.8.0** (latest stable). The PyPI documentation confirms compatibility with Datastar JS v1.0.0-RC.7 via official examples.

## Sources
- PyPI: https://pypi.org/project/datastar-py/
- Spike research: `.tf/knowledge/topics/spike-datastar-py-sanic-datastar-tf-web-ui/`
