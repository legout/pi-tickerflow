"""Ticketflow CLI - IRF workflow toolkit for Pi.

This is the canonical tf package. The tf_cli package is maintained for backward compatibility.
"""
from __future__ import annotations

# Re-export version from tf_cli for now (compatibility)
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
