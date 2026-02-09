# Comparison: textual-web vs FastAPI+HTMX

## Executive Summary

| Criteria | textual-web | FastAPI+HTMX | Winner |
|----------|-------------|--------------|--------|
| Time to MVP | Hours | Days | textual-web |
| Code Reuse | 100% (existing TUI) | 0% (new codebase) | textual-web |
| Web UX Quality | Terminal-like | Native web | FastAPI+HTMX |
| Mobile Support | Limited | Full responsive | FastAPI+HTMX |
| Accessibility | Poor | Good | FastAPI+HTMX |
| URL Routing | None | Full support | FastAPI+HTMX |
| Maintenance Burden | Low (single codebase) | High (two UIs) | textual-web |
| Future Extensibility | Limited | High | FastAPI+HTMX |

---

## Detailed Analysis

### Approach A: textual-web

#### Complexity
- **Initial Setup**: Minimal - install textual-web, create config file
- **Code Changes**: Zero - existing ui.py works as-is
- **Learning Curve**: Low - uses existing Textual knowledge
- **Infrastructure**: Simple - single command to serve

#### Maintenance
- **Single Codebase**: Terminal and web share identical code
- **Updates**: One change applies to both platforms
- **Bug Fixes**: Fix once, applies everywhere
- **Team Onboarding**: No additional skills needed

#### Features
- ✅ All existing TUI features work immediately
- ✅ Keyboard shortcuts work
- ✅ Same visual styling
- ❌ No URL routing / deep linking
- ❌ Mobile experience is suboptimal
- ❌ Requires JavaScript/WebSocket
- ❌ No graceful degradation without JS

#### Performance
- WebSocket-based communication
- Terminal rendered via xterm.js
- Slight latency compared to native web
- Color palette issues on some browsers

---

### Approach B: FastAPI+HTMX

#### Complexity
- **Initial Setup**: Moderate - new project structure, templates
- **Code Changes**: Significant - rebuild kanban UI from scratch
- **Learning Curve**: Medium - HTMX patterns, Jinja2 templates
- **Infrastructure**: Standard FastAPI deployment

#### Maintenance
- **Two Codebases**: TUI and web are separate implementations
- **Updates**: Changes must be made in both places
- **Bug Fixes**: May need fixes in both UIs
- **Team Onboarding**: Web development skills required

#### Features
- ✅ Native web UX with semantic HTML
- ✅ Bookmarkable URLs (e.g., /ticket/pt-7t1n)
- ✅ Mobile responsive design
- ✅ Works without JavaScript (basic functionality)
- ✅ Better accessibility (screen readers, etc.)
- ✅ Easy to add multi-user features later
- ❌ Different UX from terminal version
- ❌ Feature parity requires ongoing effort

#### Performance
- Server-rendered HTML
- HTMX for partial updates
- Efficient for typical kanban use
- Cachable static assets

---

## Use Case Fit

### Choose textual-web if:
- You need a working web UI **this week**
- Team is primarily terminal-focused
- Internal tool, not customer-facing
- Quick wins matter more than polish
- Want to avoid maintaining two UIs

### Choose FastAPI+HTMX if:
- Web UX is a priority
- Mobile access is important
- Accessibility requirements exist
- Public-facing or customer-facing
- Long-term web-first strategy
- Team has web development skills

---

## Recommendation

### Primary Recommendation: **FastAPI+HTMX**

Despite higher initial effort, FastAPI+HTMX is recommended for the following reasons:

1. **MVP Scope Alignment**: The MVP explicitly excludes authentication, real-time updates, and multi-user. This simplifies the FastAPI implementation significantly.

2. **Future-Proofing**: The web-native approach provides a foundation for future features (mobile app, public access, integrations) that textual-web cannot easily support.

3. **Developer Experience**: Bookmarkable URLs and responsive design make the tool more usable for the team.

4. **Technical Debt**: While textual-web is faster now, it creates a dead-end architecture. FastAPI+HTMX is an investment in sustainable growth.

### Implementation Path

**Phase 1 (MVP)**: Build FastAPI+HTMX kanban board
- Basic ticket viewing
- Manual refresh
- Localhost-only

**Phase 2**: Add essential features
- Real-time updates (SSE)
- Drag-and-drop
- Search/filter

**Phase 3**: Advanced features (future)
- Authentication
- Multi-user support
- API for integrations

### Risk Mitigation
- Keep POC code as reference
- Use existing data models (Ticket, BoardClassifier)
- Parallel development possible (TUI stays functional)

---

## Decision

**Decision**: Proceed with FastAPI+HTMX for the web UI MVP.

**Rationale**: While textual-web offers a faster path, FastAPI+HTMX better serves the long-term vision of making Ticketflow accessible via browser. The MVP scope (localhost-only, manual refresh, no auth) keeps the initial implementation manageable.

**Next Steps**:
1. Create implementation ticket for FastAPI+HTMX web UI
2. Define specific endpoints and templates needed
3. Plan feature parity with existing TUI
4. Set up basic FastAPI project structure
