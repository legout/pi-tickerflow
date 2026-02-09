# spike-datastar-py-sanic-datastar-tf-web-ui

Datastar-py is the **official Python SDK** for the Datastar hypermedia framework. It provides helpers to **generate Datastar SSE events** (patch elements, patch signals, execute scripts), **wrap responses** for popular Python web frameworks (including **Sanic**), and **read client signals**.

For the Ticketflow Sanic+Datastar web UI, you can keep the current simple `text/html` fragment approach, but adopting datastar-py becomes valuable as soon as you want **multi-target updates** (board + counts) or **server-push streaming** (auto-refresh, progress updates during Ralph runs).

## Keywords

- datastar
- datastar-py
- sanic
- sse
- html-over-the-wire
- hypermedia
- signals
- ticketflow
- web-ui
