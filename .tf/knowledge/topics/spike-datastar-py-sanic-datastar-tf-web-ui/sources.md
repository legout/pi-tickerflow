# Sources: spike-datastar-py-sanic-datastar-tf-web-ui

## Primary (Datastar / datastar-py)

- PyPI: datastar-py — https://pypi.org/project/datastar-py/
- GitHub: starfederation/datastar-python — https://github.com/starfederation/datastar-python
  - Sanic helper module: https://github.com/starfederation/datastar-python/blob/main/src/datastar_py/sanic.py
  - SSE event generator: https://github.com/starfederation/datastar-python/blob/main/src/datastar_py/sse.py
  - Sanic example app: https://github.com/starfederation/datastar-python/blob/main/examples/sanic/app.py
- GitHub: starfederation/datastar (Datastar JS) — https://github.com/starfederation/datastar
- Datastar website — https://data-star.dev

## Ticketflow repo (baseline scan)

- Current Sanic web UI: `tf_cli/web_ui.py`
- Templates:
  - `tf_cli/templates/base.html`
  - `tf_cli/templates/index.html`
  - `tf_cli/templates/_board.html`
  - `tf_cli/templates/ticket.html`
- POC README (Sanic+Datastar): `examples/web-ui-poc/sanic-datastar/README.md`
- Related prior spike: `.tf/knowledge/topics/spike-sanic-datastar-vs-fastapi-htmx/spike.md`

## Tools used

- `rg` searches in repo
- `web_search` + `fetch_content` (PyPI + GitHub + data-star.dev)
