# Backlog: spike-datastar-py-sanic-datastar-tf-web-ui

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-6hpl | Setup datastar-py dependency (pin version) for web UI | 10 | 1-2 | - | pt-4y31 |
| pt-pbpm | Add board stats DOM target for Datastar patching | 0 | 1-2 | pt-6hpl | pt-za25 |
| pt-4y31 | Implement /api/refresh as DatastarResponse (multi-target SSE patch) | 3 | 1-2 | pt-6hpl,pt-pbpm | pt-6hpl,pt-m387 |
| pt-m387 | Add /api/stream SSE endpoint (Sanic) for live board updates | 3 | 1-2 | pt-4y31 | pt-4y31,pt-za25 |
| pt-za25 | Add server-side search/filter using Datastar signals (read_signals) | 3 | 1-2 | pt-m387 | pt-m387,pt-pbpm |
