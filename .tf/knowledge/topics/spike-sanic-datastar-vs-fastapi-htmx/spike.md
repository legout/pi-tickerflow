# Spike: Sanic+Datastar vs. FastAPI+HTMX for `tf ui` web (2026)

## Summary

Ticketflow already has a **working FastAPI+HTMX proof-of-concept** (`examples/web-ui-poc/fastapi-htmx/`) and a prior spike decision (pt-7t1n) recommending FastAPI+HTMX for the MVP. This spike evaluates whether a switch to **Sanic (backend)** and **Datastar (frontend hypermedia layer)** is a better choice in 2026.

Bottom line: **Sanic+Datastar is technically feasible**, but it is **higher churn / higher risk** for Ticketflow’s current MVP goals because (a) Datastar is still shipping **1.0.0 RC releases** and has had **breaking attribute syntax changes**, and (b) FastAPI+HTMX is already proven in-repo and broadly supported. If your roadmap includes **server-push / SSE-first real-time UI** soon, Datastar becomes more compelling.

## Key Findings

1. **FastAPI remains a “safe default”** for Python web apps in 2026: mature ecosystem, excellent docs, first-class ASGI story, and strong developer tooling (typing, dependency injection, testing patterns). Ticketflow also already has a working FastAPI+HTMX POC.
   - Docs: https://fastapi.tiangolo.com/

2. **Sanic is a viable, fast async alternative**, with a long-lived community and async-first API. For Ticketflow’s SSR HTML use case, the practical benefit over FastAPI is mostly *taste/tooling*, not MVP capability.
   - Sanic repo overview: https://github.com/sanic-org/sanic

3. **Datastar’s differentiator is SSE-first “backend-driven reactivity”** (signals + DOM patching) in a single small library.
   - Datastar emphasizes `text/event-stream` and backend-driven DOM patching (`PatchElements`, `PatchSignals`): https://data-star.dev

4. **Datastar is still in 1.0.0 release candidates**, and recently introduced a **breaking change** in attribute delimiters:
   - `data-on-click` → `data-on:click`, etc. (breaking change called out in release notes)
   - This increases template churn risk for a fast-moving repo.
   - Release notes: https://github.com/starfederation/datastar/releases

5. **If you switch to Datastar, be careful about event naming and older tutorials**.
   - Example: SSE event names changed (e.g. older “merge fragments/signals” terminology vs newer `datastar-patch-elements` / `datastar-patch-signals` in release notes).

## Options Considered

### Option A — Keep FastAPI + HTMX (status quo / current decision)

**What you get**
- Already proven with an in-repo POC.
- Very low friction for implementing the current backlog (kanban, ticket detail, topic browser, inline markdown docs).
- HTMX is mature; patterns for partial updates, forms, and progressive enhancement are well-known.

**Pros**
- Lowest risk / fastest path to MVP.
- Best “Python DX” (typing, docs, common patterns).
- Many examples/boilerplates, easy onboarding.

**Cons**
- If you later want server-push realtime UI, you’ll add SSE/WS patterns on top (still doable).

**Best fit when**
- MVP is localhost-only, single-user, manual refresh (Ticketflow’s current scope).


### Option B — Switch backend only: Sanic + HTMX

**What you get**
- Keep the same hypermedia approach (HTMX), but run it on Sanic.

**Pros**
- If your team strongly prefers Sanic, this reduces backend friction.
- Minimal UI rewrite (keep HTMX templates).

**Cons**
- You lose FastAPI’s batteries-included integrations (e.g., common patterns around validation/DI/docs).
- You still need to maintain the web app code; the framework swap doesn’t add core MVP features.

**Best fit when**
- You want Sanic for internal consistency (other services already on Sanic).


### Option C — Switch backend + frontend: Sanic + Datastar

**What you get**
- An SSE-first hypermedia system that combines “HTMX-ish requests” + “Alpine-ish signals” into one small library.

**Pros**
- Datastar’s SSE + signals model can make dashboards / live boards very clean.
- Push updates from backend without user interaction (nice for kanban auto-refresh, long running operations, etc.).
- One small library and no build pipeline.

**Cons / costs**
- **Template rewrite**: replace `hx-*` attributes with `data-*` Datastar attributes.
- **Higher churn risk**: Datastar is still in RC and has shipped breaking syntax changes.
- Smaller ecosystem: fewer “copy-paste” examples, fewer proven patterns in Python-first stacks.

**Best fit when**
- You explicitly want SSE-driven UI soon (near-term) and can accept framework churn.


## Recommendation

**Recommendation for Ticketflow (MVP, 2026): Keep FastAPI+HTMX** until the web UI MVP is shipped.

Rationale:
- The repo already has a working FastAPI+HTMX POC.
- The current backlog tickets are straightforward SSR pages + partial refresh.
- Datastar is compelling, but the **RC status + recent breaking changes** are a concrete risk for a small project trying to ship quickly.

**Conditional recommendation** (when to reconsider Sanic+Datastar):
- If you decide that **server-push updates** are required for MVP (e.g. live status during Ralph runs, auto-refreshing board), then doing a *small Sanic+Datastar POC* is justified.

## Risks & Unknowns

- **Datastar API stability**: RC releases and syntax changes mean you must pin versions and expect template adjustments.
- **Python backend integration patterns**: Datastar has multiple SDKs, but Python-specific “idiomatic” examples are still fewer than HTMX’s.
- **SSE operational details**: for localhost MVP this is easy; for remote access later you’ll care about proxies/timeouts/reconnect semantics.
- **Team familiarity**: adopting Datastar introduces new mental models (signals, patch events) that aren’t HTMX’s default.

## Next Steps

1. **If you want to evaluate switching anyway (2h spike/POC):**
   - Implement a tiny `examples/web-ui-poc/sanic-datastar/` with:
     - `GET /` renders board (SSR)
     - `GET /ticket/<id>` detail view
     - A refresh button implemented in Datastar
   - Pin Datastar to a specific RC version and document the chosen attribute syntax.

2. **If staying with FastAPI+HTMX (recommended):**
   - Proceed with the existing open backlog for `seed-tf-ui-web-app`.
   - Optionally add a follow-up ticket: “Investigate SSE push updates (Datastar vs HTMX SSE extension)”.

3. **If you do switch stacks:**
   - Update `.tickets/pt-7t1n.md` notes (or create a new spike ticket) to record the new decision.
   - Update the open tickets’ text to remove FastAPI/HTMX assumptions and replace with Sanic/Datastar specifics.

