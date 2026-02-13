"""Hello-world utility for demo purposes.

This module provides a simple greeting function for demonstrating
the IRF (Implement-Review-Fix) workflow. Ticket: abc-123

The module exposes a single function `hello()` that returns a greeting
string. It can be used as a library import or run as a CLI script.

Examples:
    >>> from demo.hello import hello
    >>> hello()
    'Hello, World!'
    >>> hello("Alice")
    'Hello, Alice!'

CLI Usage:
    $ python -m demo
    Hello, World!
    $ python -m demo Alice
    Hello, Alice!
"""

from __future__ import annotations

import re


def hello(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".
            All whitespace runs (including internal) are collapsed to a single
            space, and zero-width Unicode characters (U+200B-U+200D, U+FEFF)
            are removed from anywhere in the string. Leading/trailing whitespace
            is then stripped. Empty strings and whitespace-only strings return
            the full greeting "Hello, World!".

    Returns:
        str: A greeting string in the format "Hello, {name}!".

    Raises:
        TypeError: If name is not a string type. Note: This is only raised
            when calling the function directly. The CLI interface will treat
            non-string input as a string argument and not raise TypeError.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")
    # Remove all Unicode whitespace including zero-width chars (U+200B-U+200D, U+FEFF)
    cleaned_name = re.sub(r'[\s\u200B-\u200D\uFEFF]+', ' ', name).strip()
    if not cleaned_name:
        return "Hello, World!"
    return f"Hello, {cleaned_name}!"


__all__ = ["hello"]
