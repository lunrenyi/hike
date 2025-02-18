"""Provides general application commands for the command line."""

##############################################################################
# Textual imports.
from textual.message import Message
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Help, Quit

##############################################################################
# Local imports.
from ...commands import (
    JumpToBookmarks,
    JumpToHistory,
    JumpToLocalBrowser,
    JumpToTableOfContents,
)
from .base_command import InputCommand


##############################################################################
class GeneralCommand(InputCommand):
    """Base class for general commands."""

    MESSAGE: type[Message]
    """The message to send for the command."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if cls.is_command(text):
            for_widget.post_message(cls.MESSAGE())
            return True
        return False


##############################################################################
class BookmarksCommand(GeneralCommand):
    """Jump to the bookmarks"""

    COMMAND = "`bookmarks`"
    ALIASES = "`b`, `bm`"
    MESSAGE = JumpToBookmarks


##############################################################################
class ContentsCommand(GeneralCommand):
    """Jump to the table of contents"""

    COMMAND = "`contents`"
    ALIASES = "`c`, `toc`"
    MESSAGE = JumpToTableOfContents


##############################################################################
class HelpCommand(GeneralCommand):
    """Show the help screen"""

    COMMAND = "`help`"
    ALIASES = "`?`"
    MESSAGE = Help


##############################################################################
class HistoryCommand(GeneralCommand):
    """Jump to the browsing history"""

    COMMAND = "`history`"
    ALIASES = "`h`"
    MESSAGE = JumpToHistory


##############################################################################
class LocalCommand(GeneralCommand):
    """Jump to the local file browser"""

    COMMAND = "`local`"
    ALIASES = "`l`"
    MESSAGE = JumpToLocalBrowser


##############################################################################
class QuitCommand(GeneralCommand):
    """Quit the application"""

    COMMAND = "`quit`"
    ALIASES = "`q`"
    MESSAGE = Quit


### general.py ends here
