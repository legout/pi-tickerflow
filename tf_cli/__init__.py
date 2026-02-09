"""Ticketflow CLI - IRF workflow toolkit for Pi (deprecated shim).

DEPRECATED: Use 'tf' package instead. This shim will be removed in version 0.5.0.
Set TF_CLI_DEPRECATION_WARN=1 to see warnings.
"""
from __future__ import annotations

import os
import warnings

# Emit deprecation warning if opted in (default off to avoid CI noise)
if os.environ.get("TF_CLI_DEPRECATION_WARN"):
    warnings.warn(
        "tf_cli is deprecated. Use 'tf' package instead. "
        "This shim will be removed in version 0.5.0. "
        "See https://github.com/legout/pi-ticketflow/blob/main/docs/deprecation-policy.md",
        DeprecationWarning,
        stacklevel=2,
    )

# Re-export version API from tf_cli.version for test/runtime compatibility.
from tf_cli.version import get_version, __version__
from tf.ticket_factory import (
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
