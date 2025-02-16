"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .main import (
    BookmarkLocation,
    ChangeCommandLineLocation,
    ChangeNavigationSide,
    CopyLocationToClipboard,
    CopyMarkdownToClipboard,
    Edit,
    JumpToCommandLine,
    Reload,
    SaveCopy,
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
    "CopyLocationToClipboard",
    "CopyMarkdownToClipboard",
    "Edit",
    "Forward",
    "JumpToBookmarks",
    "JumpToCommandLine",
    "JumpToHistory",
    "JumpToLocalBrowser",
    "JumpToTableOfContents",
    "Reload",
    "SaveCopy",
    "SearchBookmarks",
    "ToggleNavigation",
]

### __init__.py ends here
