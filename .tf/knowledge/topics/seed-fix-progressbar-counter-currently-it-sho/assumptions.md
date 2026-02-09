# Assumptions

- We can cheaply list the current backlog (e.g., via `tk ready` or a derived list query) without adding noticeable overhead per iteration.
- Ralph already has access to the ticket query and a way to list tickets (`ticket_list_query()`).
