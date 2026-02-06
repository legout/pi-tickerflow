"""Example script showing how to use ticket_factory for backlog generation.

This is a reference implementation that can be adapted for specific seeds,
baselines, or plans. Replace the ticket definitions and topic ID as needed.
"""

from __future__ import annotations

from tf_cli.ticket_factory import (
    TicketDef,
    create_tickets,
    write_backlog_md,
    score_tickets,
    apply_dependencies,
    apply_links,
    print_created_summary,
)


def md(parts: list[str]) -> str:
    """Helper to join markdown parts."""
    return "\n".join(parts)


# Configuration
TOPIC_ID = "seed-example-feature"

# Existing titles for de-duplication (load from backlog.md or tk list)
# existing_titles = {"example feature", "another feature"}
existing_titles = set()


# Define tickets using templates from tf-planning SKILL.md
tickets = [
    TicketDef(
        title="Setup project repository and CI pipeline",
        description=md([
            "## Task",
            "Initialize the project repository with git and CI/CD pipeline.",
            "",
            "## Context",
            "A new project needs proper version control and automated testing infrastructure.",
            "",
            "## Acceptance Criteria",
            "- [ ] Repository initialized with git",
            "- [ ] CI pipeline configured with GitHub Actions or GitLab CI",
            "- [ ] Automated tests run on push to main branch",
            "",
            "## Constraints",
            "- Use existing CI templates if available",
            "",
            "## References",
            f"- Seed: {TOPIC_ID}",
        ]),
    ),
    TicketDef(
        title="Define API contracts and data models",
        description=md([
            "## Task",
            "Define the API contracts and data models for the feature.",
            "",
            "## Context",
            "Clear contracts enable frontend and backend to work in parallel.",
            "",
            "## Acceptance Criteria",
            "- [ ] API endpoints documented with request/response schemas",
            "- [ ] Data models defined in shared types file",
            "- [ ] Validation rules specified",
            "",
            "## Constraints",
            "- Use JSON Schema or TypeScript interfaces",
            "",
            "## References",
            f"- Seed: {TOPIC_ID}",
        ]),
    ),
    TicketDef(
        title="Implement user authentication service",
        description=md([
            "## Task",
            "Implement the user authentication service with token-based auth.",
            "",
            "## Context",
            "Authentication is required for secure access to protected resources.",
            "",
            "## Acceptance Criteria",
            "- [ ] Login endpoint accepts username/password",
            "- [ ] JWT token generation and validation",
            "- [ ] Token refresh mechanism",
            "",
            "## Constraints",
            "- Store passwords securely (hashed)",
            "",
            "## References",
            f"- Seed: {TOPIC_ID}",
        ]),
    ),
    TicketDef(
        title="Write tests for authentication flow",
        description=md([
            "## Task",
            "Add comprehensive tests for the authentication service.",
            "",
            "## Context",
            "Tests ensure authentication works correctly and security is maintained.",
            "",
            "## Acceptance Criteria",
            "- [ ] Unit tests for token generation/validation",
            "- [ ] Integration tests for login endpoint",
            "- [ ] Edge cases covered (invalid credentials, expired tokens)",
            "",
            "## Constraints",
            "- Use pytest and mocking for external dependencies",
            "",
            "## References",
            f"- Seed: {TOPIC_ID}",
        ]),
    ),
]


def main() -> int:
    """Run the ticket creation process."""
    # Score tickets by keyword (setup=10, configure=8, define=6, design=5, implement=3, test=1)
    scored = score_tickets(tickets)

    # Create tickets
    print(f"Creating tickets for {TOPIC_ID}...\n")
    created = create_tickets(
        scored,
        topic_id=TOPIC_ID,
        mode="seed",
        component_tags=True,  # Auto-assign component:cli, component:tests, etc.
        existing_tickets=existing_titles,
        priority=2,
        dry_run=False,  # Set to True to test without creating
    )

    # Apply dependencies (chain mode: each ticket depends on previous)
    created = apply_dependencies(created, mode="chain")

    # Apply links between related tickets
    created = apply_links(created)

    # Write backlog.md
    backlog_path = write_backlog_md(created, topic_id=TOPIC_ID)
    print(f"\nBacklog written to: {backlog_path}")

    # Print summary
    print_created_summary(created)

    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
