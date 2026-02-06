"""Knowledge base management CLI commands.

Implements the tf kb command for managing the knowledge base:
- ls: List knowledge base entries
- show: Show a specific knowledge entry
- index: Manage the knowledge base index
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

from tf_cli.kb_helpers import (
    atomic_read_index,
    atomic_write_index,
    resolve_knowledge_dir,
)


def cmd_ls(knowledge_dir: Path, format_json: bool = False) -> int:
    """List knowledge base entries from index.json."""
    data = atomic_read_index(knowledge_dir)

    if data is None:
        if format_json:
            print(json.dumps({"entries": []}))
        else:
            print("No knowledge base index found.")
            print(f"Expected: {knowledge_dir / 'index.json'}")
        return 0

    entries = data.get("entries", [])

    if format_json:
        print(json.dumps({"entries": entries}, indent=2))
    else:
        if not entries:
            print("Knowledge base is empty.")
        else:
            print(f"Knowledge base entries ({len(entries)} total):")
            print()
            for entry in entries:
                if isinstance(entry, dict):
                    entry_id = entry.get("id", "unknown")
                    title = entry.get("title", "Untitled")
                    entry_type = entry.get("type", "unknown")
                    print(f"  {entry_id} [{entry_type}] - {title}")
                else:
                    print(f"  {entry}")

    return 0


def cmd_show(knowledge_dir: Path, entry_id: str, format_json: bool = False) -> int:
    """Show a specific knowledge base entry."""
    data = atomic_read_index(knowledge_dir)

    if data is None:
        print(f"Error: Knowledge base index not found at {knowledge_dir / 'index.json'}", file=sys.stderr)
        return 1

    entries = data.get("entries", [])

    # Find entry by id
    entry = None
    for e in entries:
        if isinstance(e, dict) and e.get("id") == entry_id:
            entry = e
            break

    if entry is None:
        print(f"Error: Entry '{entry_id}' not found in knowledge base.", file=sys.stderr)
        return 1

    if format_json:
        print(json.dumps(entry, indent=2))
    else:
        print(f"ID: {entry.get('id', 'unknown')}")
        print(f"Type: {entry.get('type', 'unknown')}")
        print(f"Title: {entry.get('title', 'Untitled')}")
        if "path" in entry:
            print(f"Path: {entry['path']}")
        if "created" in entry:
            print(f"Created: {entry['created']}")
        if "updated" in entry:
            print(f"Updated: {entry['updated']}")
        if "tags" in entry:
            print(f"Tags: {', '.join(entry['tags'])}")

    return 0


def cmd_index_status(knowledge_dir: Path, format_json: bool = False) -> int:
    """Show knowledge base index status."""
    index_path = knowledge_dir / "index.json"
    data = atomic_read_index(knowledge_dir)

    if data is None:
        if format_json:
            print(json.dumps({"status": "not_found", "path": str(index_path), "entries": 0}))
        else:
            print(f"Knowledge base index: NOT FOUND")
            print(f"Expected path: {index_path}")
        return 1

    entries = data.get("entries", [])
    entry_count = len(entries)

    if format_json:
        print(json.dumps({"status": "ok", "path": str(index_path), "entries": entry_count}))
    else:
        print(f"Knowledge base index: OK")
        print(f"Path: {index_path}")
        print(f"Entries: {entry_count}")
    return 0


def usage() -> None:
    """Print usage information."""
    print(
        """Knowledge base management commands.

Usage:
  tf kb ls [--json] [--knowledge-dir <path>]
  tf kb show <entry-id> [--json] [--knowledge-dir <path>]
  tf kb index [--knowledge-dir <path>]
  tf kb --help

Commands:
  ls          List all knowledge base entries
  show        Show details for a specific entry
  index       Show index status and statistics

Options:
  --json      Output in JSON format
  --knowledge-dir <path>  Use specific knowledge directory
"""
    )


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for kb CLI."""
    if argv is None:
        argv = sys.argv[1:]
    
    # Handle help/usage
    if not argv or argv[0] in {"-h", "--help", "help"}:
        usage()
        return 0
    
    # Parse global options
    knowledge_dir_override: Optional[Path] = None
    format_json = False
    
    # Extract global flags before subcommand parsing
    filtered_argv = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--json":
            format_json = True
        elif arg == "--knowledge-dir" and i + 1 < len(argv):
            knowledge_dir_override = Path(argv[i + 1]).expanduser()
            i += 1
        else:
            filtered_argv.append(arg)
        i += 1
    
    if not filtered_argv:
        usage()
        return 0
    
    command = filtered_argv[0]
    rest = filtered_argv[1:]
    
    # Resolve knowledge directory with CLI override support
    knowledge_dir = resolve_knowledge_dir(knowledge_dir_override=knowledge_dir_override)
    
    # Dispatch commands
    if command == "ls":
        return cmd_ls(knowledge_dir, format_json=format_json)
    
    if command == "show":
        if not rest or rest[0].startswith("-"):
            print("Error: Entry ID required for 'show' command", file=sys.stderr)
            print("Usage: tf kb show <entry-id>", file=sys.stderr)
            return 1
        entry_id = rest[0]
        return cmd_show(knowledge_dir, entry_id, format_json=format_json)
    
    if command == "index":
        return cmd_index_status(knowledge_dir, format_json=format_json)
    
    print(f"Unknown 'kb' subcommand: {command}", file=sys.stderr)
    usage()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
