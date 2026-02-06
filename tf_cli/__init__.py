"""Ticketflow CLI - IRF workflow toolkit for Pi."""
from __future__ import annotations

from tf_cli.version import get_version, __version__

# Re-export ticket_factory for convenience
from tf_cli.ticket_factory import (
    TicketDef,
    CreatedTicket,
    apply_dependencies,
    apply_links,
    create_tickets,
    print_created_summary,
    score_tickets,
    write_backlog_md,
)

__all__ = [
    "__version__",
    "get_version",
    # ticket_factory exports
    "TicketDef",
    "CreatedTicket",
    "apply_dependencies",
    "apply_links",
    "create_tickets",
    "print_created_summary",
    "score_tickets",
    "write_backlog_md",
]