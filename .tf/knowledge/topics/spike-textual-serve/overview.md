# spike-textual-serve

Research findings on using Textual’s **`textual serve`** (devtools) to run a Textual TUI in the browser.

## Quick Answer

Yes: Textual apps can be served in a browser using `textual serve`, typically as:

```bash
textual serve "python -m tf_cli.ui"
```

This starts a web server (default `localhost:8000`) and proxies user input/output over WebSockets so the app continues to run server-side.

## Keywords

- textual
- textual-serve
- textual-dev
- web
- websocket
- tf-cli-ui
