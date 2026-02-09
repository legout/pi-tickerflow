"""Module entrypoint for python -m tf_cli.

DEPRECATED: Use 'python -m tf' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

import os
import sys
import warnings

# Emit deprecation warning if opted in (default off to avoid CI noise)
if os.environ.get("TF_CLI_DEPRECATION_WARN"):
    warnings.warn(
        "python -m tf_cli is deprecated. Use 'python -m tf' instead. "
        "This shim will be removed in version 0.5.0. "
        "See https://github.com/legout/pi-ticketflow/blob/main/docs/deprecation-policy.md",
        DeprecationWarning,
        stacklevel=2,
    )

from tf.cli import main

if __name__ == "__main__":
    sys.exit(main())
