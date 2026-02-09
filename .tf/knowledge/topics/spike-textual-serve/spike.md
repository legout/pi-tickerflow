# Spike: `textual serve`

## Summary

`textual serve` is part of Textual’s devtools CLI and can serve a Textual app to a browser, effectively turning a terminal-first UI into something accessible over HTTP/WebSockets. Under the hood, Textualize’s `textual-serve` project runs your app in a subprocess and bridges it via a WebSocket protocol; it is not “a shell in the browser”, it’s a Textual-specific protocol.

In this repo, the UI entry point `python -m tf_cli.ui` already contains a non-TTY warning path, which is a good sign for compatibility with web serving. Additionally, there is already a working proof-of-concept for **`textual-web`** (a related tool that provides public URLs), which suggests web-serving the app is feasible with little/no code change.

## Key Findings

1. **`textual serve` can serve apps launched from a Python file or from a command.**
   - For commands / module execution, the docs explicitly show providing a full command string (including `python -m ...`).

2. **Defaults are local-first (typically `localhost:8000`) and the server speaks WebSockets.**
   - Users open the printed link in a browser; the app continues executing on the host machine.

3. **`textual-serve` is the self-hosted building block behind the “serve in browser” experience.**
   - It launches the app in a subprocess and brokers I/O over a websocket.

4. **`textual-web` is a sibling tool that can publish apps/terminals to public URLs.**
   - It can expose a Textual app or even a full terminal session; it includes an explicit warning not to share terminal URLs with untrusted parties.

5. **Repo-specific evidence:**
   - `tf_cli/ui.py` acknowledges non-TTY execution and doesn’t hard-fail when stdin/stdout aren’t TTYs.
   - There’s an existing POC under `examples/web-ui-poc/textual-web/` showing `textual-web --config …` serving `python -m tf_cli.ui`.

## Options Considered

### Option A — Support `textual serve` (Textual devtools)

**What it is:** A Textual-provided CLI subcommand to serve a Textual app to a browser.

**Pros**
- Minimal app changes (often zero if the app is already runnable).
- Local-first defaults are relatively safe.
- Simple user story: run one command, click link.

**Cons / gotchas**
- Browser UX is still “terminal-like” (not a native web SPA).
- Requires JS + WebSockets.
- If users bind publicly (e.g., `--host 0.0.0.0`), security posture becomes important.

**Likely command for this repo**
```bash
textual serve "python -m tf_cli.ui"
```

### Option B — Use `textual-web` (public URLs / publishing)

**What it is:** A tool for publishing Textual apps (and terminals) on the web with public URLs, configured via TOML.

**Pros**
- Designed for sharing with others (public URL workflows).
- Multi-app configuration and stable slugs (via account) are supported.

**Cons / gotchas**
- Public URLs are inherently riskier.
- Serving a terminal is explicitly dangerous if shared.
- Adds operational questions (accounts, permanence, who can access).

**Repo POC**
```bash
textual-web --config examples/web-ui-poc/textual-web/serve.toml
```

### Option C — Build a dedicated web UI

**Pros**
- Best web UX, routing, deep links, auth, etc.

**Cons**
- Larger scope; not aligned with “enable `textual serve`”.

## Recommendation

For the seed goal (“serve the Textual app as a web app using `textual serve`”):

1. **Document an officially supported command** (`textual serve "python -m tf_cli.ui"`).
2. **Add a small wrapper command** (future work) like `tf ui --web` that prints the exact `textual serve …` invocation (or calls into `textual-serve` programmatically).
3. **Keep defaults local-only** and require explicit opt-in for public binding; add a warning banner/message when binding to non-localhost.
4. Keep `textual-web` as an advanced/experimental option (POC exists) for public sharing.

## Risks & Unknowns

- Mobile/latency experience may vary (Textual-web README notes variability on mobile).
- If serving beyond localhost, we likely need guidance or constraints (auth, reverse proxy, network ACLs).
- Exact CLI flags for `textual serve` may differ by Textual version; documentation should reference “run `textual serve --help`”.

## Next Steps

- Add a follow-up ticket to validate `textual serve "python -m tf_cli.ui"` works end-to-end.
- Decide whether to vendor a `serve.toml` example for `textual-web` (optional).
- If needed, add small code changes in `tf_cli/ui.py` to improve non-TTY / web-session behavior (logging, shutdown semantics).
