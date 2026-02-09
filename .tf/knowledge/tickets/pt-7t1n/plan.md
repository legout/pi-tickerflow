# Plan: pt-7t1n Spike - Evaluate textual-web vs FastAPI+HTMX

## Objective
Build proof-of-concepts for both approaches and document a clear recommendation for the tf web UI.

## Deliverables
1. **POC 1: textual-web** - Minimal wrapper to serve existing ui.py via textual-web
2. **POC 2: FastAPI+HTMX** - Basic web app with kanban view using FastAPI and HTMX
3. **Comparison Document** - Analysis of complexity, maintenance, features, performance
4. **Recommendation** - Clear decision with justification

## Implementation Steps

### Phase 1: textual-web POC
- Install textual-web
- Create minimal wrapper script
- Test serving existing TUI in browser
- Document findings

### Phase 2: FastAPI+HTMX POC
- Set up FastAPI project structure
- Create kanban board template with HTMX
- Implement ticket data endpoint
- Test functionality
- Document findings

### Phase 3: Analysis & Recommendation
- Compare both approaches
- Document pros/cons
- Make recommendation
- Create follow-up tickets for implementation

## Technical Approach
Keep both POCs minimal but functional - kanban board display is the minimum viable feature.
