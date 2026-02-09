"""Compatibility shim for deprecated tf_cli.frontmatter module.

DEPRECATED: Use 'tf.frontmatter' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.frontmatter import *  # noqa: F401,F403
