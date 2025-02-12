"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .bookmarks import Bookmark, Bookmarks, load_bookmarks, save_bookmarks
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
    "Bookmark",
    "Bookmarks",
    "Configuration",
    "load_bookmarks",
    "load_configuration",
    "load_history",
    "save_bookmarks",
    "save_configuration",
    "save_history",
    "update_configuration",
]

### __init__.py ends here
