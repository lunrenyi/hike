"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .history import load_history, save_history

##############################################################################
# Exports.
__all__ = [
    "Configuration",
    "load_configuration",
    "load_history",
    "save_configuration",
    "save_history",
    "update_configuration",
]

### __init__.py ends here
