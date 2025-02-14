"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .main import (
    BookmarkLocation,
    ChangeCommandLineLocation,
    ChangeNavigationSide,
    JumpToCommandLine,
    Reload,
    SearchBookmarks,
    ToggleNavigation,
)
from .navigation import (
    Backward,
    Forward,
    JumpToBookmarks,
    JumpToHistory,
    JumpToLocalBrowser,
    JumpToTableOfContents,
)

##############################################################################
# Exports.
__all__ = [
    "Backward",
    "BookmarkLocation",
    "ChangeCommandLineLocation",
    "ChangeNavigationSide",
    "Forward",
    "JumpToBookmarks",
    "JumpToCommandLine",
    "JumpToHistory",
    "JumpToLocalBrowser",
    "JumpToTableOfContents",
    "Reload",
    "SearchBookmarks",
    "ToggleNavigation",
]

### __init__.py ends here
