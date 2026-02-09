# Sources

## Selected Stack (Decision: pt-sd01)

### Sanic
- Sanic Documentation: https://sanic.dev/
- Sanic GitHub: https://github.com/sanic-org/sanic
- Sanic Jinja2 Integration: https://sanic.dev/en/guide/how-to/templating.html

### Datastar
- Datastar Website: https://data-star.dev
- Datastar GitHub: https://github.com/starfederation/datastar
- Datastar Python SDK: https://github.com/starfederation/datastar/tree/main/sdk/python
- CDN Bundle (pinned): `https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-RC.7/bundles/datastar.js`

## Alternative Stacks (Evaluated)

### Textual Web
- Textual Web Announcement: https://textual.textualize.io/blog/2023/09/06/textual-web/
- Textual Web Documentation: https://textual.textualize.io/guide/web/
- GitHub: https://github.com/Textualize/textual-web

### FastAPI + HTMX
- FastAPI Documentation: https://fastapi.tiangolo.com/
- HTMX Documentation: https://htmx.org/docs/
- POC available at: `examples/web-ui-poc/fastapi-htmx/`

## Related Code
- `tf_cli/ui.py` - Current Textual TUI implementation
- `tf_cli/ticket_loader.py` - Ticket loading logic (can be reused)
- `tf_cli/board_classifier.py` - Board classification logic (can be reused)
- `examples/web-ui-poc/sanic-datastar/` - POC implementation (Sanic+Datastar)

## Similar Projects
- Jupyter Notebook web interface
- GitHub Codespaces web terminal
- VS Code Server / code-server
