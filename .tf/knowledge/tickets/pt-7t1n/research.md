# Research: pt-7t1n - Web UI Approaches

## textual-web (textual-serve)

### Overview
Textual Web is a tool to serve Textual TUI applications in a web browser. The app runs on a server and communicates with the browser via WebSocket.

**Repository**: https://github.com/Textualize/textual-web

### Installation
```bash
pipx install textual-web
# or
pip install textual-web
```

### How It Works
- Textual app runs on the server (not in browser)
- Communication via custom protocol over WebSocket
- Browser renders using xterm.js (same as VS Code terminal)
- ANSI escape codes flow between browser and server

### Configuration
Create a `serve.toml` file:
```toml
[app.Ticketflow]
command = "python -m tf_cli.ui"
slug = "tf"
```

Run with:
```bash
textual-web --config serve.toml
```

### Web-Specific Features (Recent)
- `App.open_url()` - Opens links in user's browser (not server)
- `App.deliver_text()` / `App.deliver_binary()` - File downloads in browser
- Works seamlessly across terminal and web

### Pros
- **Minimal code changes** - existing ui.py works as-is
- **Single codebase** - no separate web implementation
- **Fastest time-to-market** - can work within hours
- **All TUI features work** - including existing key bindings

### Cons
- **Terminal-like UX in browser** - not native web feel
- **Mobile experience varies** - iPhone okay, others may have issues
- **Color palette issues** - upstream library bug with extensive colors
- **No URL routing** - can't bookmark specific views
- **Single-user focus** - sessions not yet implemented (closing tab kills app)
- **WebSocket required** - won't work without JavaScript

---

## FastAPI + HTMX

### Overview
Build a web-native interface with FastAPI backend and HTMX for dynamic server-rendered updates.

### Installation
```bash
pip install fastapi uvicorn jinja2
```

### How It Works
- FastAPI serves HTML templates with Jinja2
- HTMX adds AJAX-like interactions without JavaScript
- Server returns HTML fragments for updates
- `HX-Request` header detection for fragment vs full page

### Basic Structure
```python
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        return templates.TemplateResponse("kanban_board.html", {...})
    return templates.TemplateResponse("index.html", {...})
```

### Template Structure
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
<div id="kanban-board" hx-get="/board" hx-trigger="load">
    {% for col_id, col in columns.items() %}
    <div class="column" id="col-{{ col.id }}">
        <h2>{{ col.title }}</h2>
        <!-- tasks here -->
    </div>
    {% endfor %}
</div>
```

### Pros
- **Native web UX** - feels like a real web app
- **Bookmarkable URLs** - /tickets/pt-7t1n works
- **Better accessibility** - standard HTML
- **Mobile responsive** - can be designed for all devices
- **Graceful degradation** - works without JavaScript (basic)
- **Extensible** - easy to add multi-user later

### Cons
- **Separate codebase** - doesn't reuse existing TUI code
- **More initial work** - need to rebuild kanban UI
- **Two languages** - Python + HTML templates
- **Learning curve** - HTMX patterns for team

---

## Sources
- https://github.com/Textualize/textual-web
- https://textual.textualize.io/blog/2024/09/08/towards-textual-web-applications/
- https://testdriven.io/blog/fastapi-htmx/
