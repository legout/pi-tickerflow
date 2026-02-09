# spike-sanic-datastar-vs-fastapi-htmx

Research spike: compare **Sanic+Datastar** vs **FastAPI+HTMX** for implementing `tf ui` as a localhost web app in **2026**.

## Quick Answer

For **Ticketflow’s current MVP goals** (localhost-only, single-user, manual refresh, SSR HTML), **FastAPI+HTMX remains the lowest-risk choice**: it’s widely adopted, tooling is excellent, and the repo already contains a working FastAPI+HTMX POC.

**Sanic+Datastar is viable**—and especially interesting if you want **server-push UX via SSE** and “signals”-style UI state—however **Datastar is still in 1.0.0 RC releases** and has had **breaking attribute syntax changes** (e.g. `data-on-click` → `data-on:click`), which increases churn risk for templates.

## Keywords

- sanic
- fastapi
- datastar
- htmx
- html-over-the-wire
- sse
- templates
- web-ui
- hypermedia
