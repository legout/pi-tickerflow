"""Workflow status utility - quick overview of IRF workflow state."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Optional

# Use existing frontmatter pattern from ticket_loader
FRONTMATTER_PATTERN = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", re.DOTALL)

logger = logging.getLogger(__name__)


class WorkflowStats(NamedTuple):
    """Statistics about the current workflow state."""
    open_tickets: int
    ready_tickets: int
    in_progress: int
    recent_closed: int
    has_ralph: bool
    knowledge_entries: int


@dataclass
class WorkflowStatus:
    """Complete workflow status report."""
    stats: WorkflowStats
    project_root: Path
    config_exists: bool


def _parse_frontmatter_status(content: str) -> tuple[str, list[str]] | None:
    """Extract status and deps from frontmatter using proper regex.
    
    Returns:
        Tuple of (status, deps_list) or None if no frontmatter found.
    """
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None
    
    frontmatter = match.group(1)
    status = "unknown"
    deps: list[str] = []
    
    for line in frontmatter.split("\n"):
        line = line.strip()
        if line.startswith("status:"):
            status = line.split(":", 1)[1].strip()
        elif line.startswith("deps:"):
            value = line.split(":", 1)[1].strip()
            if value.startswith("[") and value.endswith("]"):
                # Parse [item1, item2]
                deps = [d.strip().strip('"\'') for d in value[1:-1].split(",") if d.strip()]
            elif value == "[]":
                deps = []
    
    return status, deps


def count_tickets_by_status(tickets_dir: Path) -> dict[str, int]:
    """Count tickets by their status from frontmatter."""
    counts = {"open": 0, "ready": 0, "in_progress": 0, "closed": 0}
    
    if not tickets_dir.exists():
        return counts
    
    for ticket_file in tickets_dir.glob("*.md"):
        try:
            # Read only first 2KB for frontmatter (efficient)
            content = ticket_file.read_bytes()[:2048].decode("utf-8", errors="ignore")
            
            parsed = _parse_frontmatter_status(content)
            if parsed is None:
                continue
                
            status, deps = parsed
            
            if status == "open":
                counts["open"] += 1
                # Ready = open with no unresolved dependencies
                if len(deps) == 0:
                    counts["ready"] += 1
            elif status == "closed":
                counts["closed"] += 1
            elif status == "in_progress":
                counts["in_progress"] += 1
        except (IOError, OSError) as e:
            logger.warning(f"Could not read ticket {ticket_file.name}: {e}")
            continue
    
    return counts


def get_knowledge_entries(knowledge_dir: Path) -> int:
    """Count knowledge base entries."""
    if not knowledge_dir.exists():
        return 0
    
    entries = 0
    for subdir in ["topics", "spikes", "tickets"]:
        subpath = knowledge_dir / subdir
        if subpath.exists():
            entries += len([x for x in subpath.iterdir() if x.is_dir()])
    
    return entries


def _resolve_project_root(cwd: Path | None = None) -> Path:
    """Find project root by looking for .tf directory.
    
    Uses the same pattern as TicketLoader._resolve_tickets_dir().
    """
    cwd = cwd or Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".tf").is_dir():
            return parent
    return cwd


def get_workflow_status(project_root: Path | str | None = None) -> WorkflowStatus:
    """Get complete workflow status for the project."""
    if project_root is None:
        project_root = _resolve_project_root()
    
    project_root = Path(project_root)
    tf_dir = project_root / ".tf"
    # Tickets are in .tickets/ at project root, not .tf/tickets/
    tickets_dir = project_root / ".tickets"
    knowledge_dir = tf_dir / "knowledge"
    ralph_dir = tf_dir / "ralph"
    
    ticket_counts = count_tickets_by_status(tickets_dir)
    
    stats = WorkflowStats(
        open_tickets=ticket_counts["open"],
        ready_tickets=ticket_counts["ready"],
        in_progress=ticket_counts["in_progress"],
        recent_closed=ticket_counts["closed"],
        has_ralph=ralph_dir.exists(),
        knowledge_entries=get_knowledge_entries(knowledge_dir),
    )
    
    return WorkflowStatus(
        stats=stats,
        project_root=project_root,
        config_exists=(tf_dir / "config" / "settings.json").exists(),
    )


def print_status(status: WorkflowStatus | None = None) -> None:
    """Print formatted workflow status to stdout."""
    if status is None:
        status = get_workflow_status()
    
    print("\n🔧 TF Workflow Status")
    print("=" * 40)
    print(f"📁 Project: {status.project_root}")
    print(f"⚙️  Config: {'✅' if status.config_exists else '❌'}")
    print()
    print("📊 Tickets")
    print(f"   Open:       {status.stats.open_tickets}")
    print(f"   Ready:      {status.stats.ready_tickets}")
    print(f"   In Progress:{status.stats.in_progress}")
    print(f"   Closed:     {status.stats.recent_closed}")
    print()
    print("📚 Knowledge Base")
    print(f"   Entries:    {status.stats.knowledge_entries}")
    print()
    print("🤖 Ralph Loop")
    print(f"   Status:     {'✅ Active' if status.stats.has_ralph else '❌ Not configured'}")
    print("=" * 40)


if __name__ == "__main__":
    print_status()
