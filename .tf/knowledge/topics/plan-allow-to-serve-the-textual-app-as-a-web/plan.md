---
id: plan-allow-to-serve-the-textual-app-as-a-web
status: approved
last_updated: 2026-02-09
---

# Plan: Serve the Ticketflow Textual UI in a browser via `textual serve`

## Summary

Add first-class support and documentation for running the existing Textual TUI (`tf_cli.ui`) in a browser using Textual devtools’ `textual serve`. The goal is a low-effort way to access the UI without a local terminal UI, while keeping the default posture safe (local-only) and ensuring we don’t regress the standard terminal execution path.

This plan focuses on “make it work, document it, and guard-rail it”. It does **not** attempt to build a native web UI.

## Inputs / Related Topics

- Root Seed: [seed-allow-to-serve-the-textual-app-as-a-web](topics/seed-allow-to-serve-the-textual-app-as-a-web/seed.md)
- Session: seed-allow-to-serve-the-textual-app-as-a-web@2026-02-09T10-51-55Z
- Related Spikes:
  - [spike-textual-serve](topics/spike-textual-serve/spike.md)

## Requirements

- Document **officially supported** ways to start the UI in web mode:
  - **Installed CLI**: `textual serve "tf ui"`
  - **From repo / dev checkout**: `textual serve "python -m tf_cli.ui"` (fallback if `tf` isn’t on PATH)
- Web mode must not break terminal mode execution (`tf ui` and `python -m tf_cli.ui`).
- Documentation must include prerequisites and discoverability:
  - The `textual` CLI comes from **`textual-dev`** (tell users to install it if `textual` isn’t found).
  - Point users to `textual serve --help` for the authoritative list of flags (host/port, etc.).
- Safe-by-default guidance:
  - Document that **localhost binding is the supported default**.
  - If users bind to non-localhost / `0.0.0.0`, documentation must include a prominent warning and basic mitigations (don’t expose publicly; use firewall/VPN/reverse proxy/auth as appropriate).
- Non-TTY behavior definition (“reasonable logging”):
  - App should not crash when stdin/stdout aren’t TTYs.
  - A **single warning to stderr** is acceptable; avoid noisy stdout output.
- Verification definition (“basic smoke test”):
  - Automated smoke test that `import tf_cli.ui` succeeds in CI/headless contexts.
  - Manual checklist for web mode (start server, load UI in browser, basic navigation, shutdown expectations).
- Document current session lifecycle behavior:
  - If closing the browser tab terminates the app process, document that explicitly (so users don’t assume persistence).

## Constraints

- Keep changes minimal; do not redesign the UI.
- Avoid introducing new heavy runtime dependencies.
- Maintain backwards compatibility with existing Textual/TUI usage.

## Assumptions

- Textual + textual-dev are already part of the supported toolchain.
- `tf ui` is the user-facing entry point; `python -m tf_cli.ui` remains a supported fallback for dev/source checkouts.
- Most users will run web mode locally; public exposure is an advanced scenario.

## Risks & Gaps

- Security: binding to a public interface without auth could expose the UI to unintended users.
  - Mitigation: make localhost the documented default; include prominent warnings + basic mitigations (don’t expose publicly; use firewall/VPN/SSH tunnel/reverse proxy/auth).
- Version drift: `textual serve` flags/behavior may change across Textual versions.
  - Mitigation: document `textual serve --help` as the source of truth; keep docs concise; pin minimum versions in packaging.
- UX limitations: web-served UI is still terminal-like; mobile behavior may be inconsistent.
  - Mitigation: explicitly set expectations; keep web mode positioned as “accessibility / remote convenience”, not a native web UI.
- Asset routing: if themes/CSS are loaded from relative paths, they may not resolve correctly under the proxy/path behavior of `textual serve`.
  - Mitigation: verify in Phase 1; if needed, switch to package resources / absolute paths.
- Shutdown handling: closing the browser tab currently kills the app process; this may confuse users or lose in-flight edits.
  - Mitigation: document lifecycle clearly; consider adding an in-app message/status indicator in web mode (future enhancement).
- Dependency confusion: users might conflate `textual serve` (local) with `textual-web` (public URLs) and accidentally expose their UI.
  - Mitigation: docs must clearly separate the two; keep `textual-web` as “experimental / advanced” unless explicitly supported.
- CLI discoverability: the plan assumes users will run `python -m tf_cli.ui`, but the primary CLI entry point is `tf`.
  - Mitigation: prefer `textual serve "tf ui"` in docs, and keep module invocation as fallback.

## Work Plan (phases / tickets)

1. **Verify baseline behavior**
   - Validate both web-mode invocations:
     - `textual serve "tf ui"`
     - `textual serve "python -m tf_cli.ui"`
   - Capture known limitations (latency, browser quirks, asset loading, shutdown behavior when tab closes).

2. **Add docs + official guidance**
   - Add a short “Web mode” section to README.md (or the primary user docs entry point) with:
     - prerequisites: `textual-dev` (for `textual` CLI) + project install steps
     - exact commands to run (installed + dev fallback)
     - expected URL output (default `http://localhost:8000`)
     - host/port customization note (point to `textual serve --help`)
     - explicit warning + best practices if binding beyond localhost
     - note about lifecycle (what happens when browser tab closes)

3. **Add guard rails for non-local binding**
   - Keep guardrails lightweight (docs + warnings).
   - If we add any wrapper flags, ensure we:
     - default to localhost
     - emit a prominent warning when binding beyond localhost
     - do **not** attempt to implement authentication in this scope

4. **Optional: convenience wrapper command (keep minimal)**
   - Add a `tf ui --web` (or similar) that prints (or launches) the correct `textual serve …` command.
   - Keep it thin: avoid re-implementing serving; do not add config parsing, auth, or process management beyond printing the command.

5. **Test/CI smoke coverage**
   - Add a minimal smoke test that asserts `import tf_cli.ui` succeeds in CI/headless (non-TTY) contexts.
   - Optionally (if stable), add a very small subprocess-based check that `python -m tf_cli.ui --help` (or similar non-interactive flag) exits 0.
   - Document a manual verification checklist for web mode (start, load in browser, basic navigation, stop server).

## Acceptance Criteria

- [ ] Documentation exists showing how to run the UI in the browser via `textual serve`.
- [ ] Docs include both command variants:
  - [ ] `textual serve "tf ui"`
  - [ ] `textual serve "python -m tf_cli.ui"` (dev fallback)
- [ ] The documented command works on a clean checkout with declared dependencies.
- [ ] Terminal mode remains functional (no regressions).
- [ ] Safety guidance exists for non-localhost binding (warning + best practices).
- [ ] Docs explicitly state lifecycle behavior (what happens when the browser tab closes).
- [ ] Web mode loads with correct styling (no missing CSS/theme regressions) and basic navigation works.
- [ ] A basic smoke test or documented verification checklist exists.
- [ ] CI still passes and `import tf_cli.ui` works in a headless (non-TTY) context without raising.

## Open Questions

- Do we want to officially support `textual-web` (public URLs) or keep it as experimental/POC-only?
- Do we need any authentication story for public binding, or is “local-only supported” sufficient?
- Should we add a dedicated config file / env vars for host/port, or rely on `textual serve` CLI options?

---

## Consultant Notes (Metis)

- 2026-02-09: Draft created from active planning session seed + spike; ensure doc wording is explicit about local-only being the supported default.
- 2026-02-09: Consultation pass:
  - Added gaps: Asset routing, Shutdown handling, Dependency confusion (textual-web vs textual serve), CLI entry-point alignment.
  - Added acceptance criteria: CI/headless import smoke test.
  - Clarified guardrails as docs/warnings, not hard blocks.
  - Flagged over-engineering risk: keep wrapper minimal (print command only); avoid config parsers, auth, process management.
  - Flagged ambiguity: define “basic smoke test” as import-safety + build health; define “reasonable logging” as non-TTY warning only.
- 2026-02-09: Revision pass:
  - Clarified requirements with explicit definitions for “reasonable logging” and “basic smoke test”.
  - Switched docs to prefer user-facing entry point `tf ui` while keeping `python -m tf_cli.ui` as dev fallback.
  - Added explicit doc requirements for lifecycle/shutdown behavior and non-local binding warnings.
  - Tightened wrapper scope to avoid scope creep.

## Reviewer Notes (Momus)

- 2026-02-09: PASS
  - Blockers:
    - (none)
  - Required changes:
    - (none)
  - Notes / suggestions:
    - Keep `textual-web` explicitly out-of-scope unless you decide to support it; otherwise it may confuse users and weaken the security posture.
    - When writing docs, include copy/paste examples for both installed and dev scenarios, and a one-line warning about not binding publicly.
