# Seed: allow to serve the textual app as a web app using `textual serve`

## Vision

Make the Textual UI accessible through a browser by supporting `textual serve` as a first-class way to run the app. This lowers the barrier for users who can’t (or don’t want to) run a terminal UI locally, and enables lightweight remote usage.

## Core Concept

Package/launch the current Textual `App` so it can be started via Textual’s web serving mode (`textual serve …`), including any needed adjustments for static assets, configuration, and networking.

## Key Features

1. Documented workflow: how to start the app in web mode and how to access it.
2. A stable entry point for running the app under `textual serve` (module path or script).
3. Basic configuration support (host/port, bind address, auth expectations if any).

## Open Questions

- Do we need to support remote access (bind 0.0.0.0) or local-only by default?
- Should web mode require authentication / a warning banner if bound publicly?
- Do we need different settings for terminal vs web (e.g., keybindings, clipboard)?
- Are there assets/files that must be served (themes, icons, CSS) and where should they live?
