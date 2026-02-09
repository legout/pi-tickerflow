"""Compatibility shim for deprecated tf_cli.project_bundle module.

DEPRECATED: Use 'tf.project_bundle' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.project_bundle import *  # noqa: F401,F403
from tf.project_bundle import compute_bundle_plan
from tf.project_bundle import __all__ as _PROJECT_BUNDLE_ALL

__all__ = list(_PROJECT_BUNDLE_ALL)
if "compute_bundle_plan" not in __all__:
    __all__.append("compute_bundle_plan")
