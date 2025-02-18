"""Provides general application commands for the command line."""

##############################################################################
# Textual imports.
from textual.message import Message
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Quit

##############################################################################
# Local imports.
from ...commands import JumpToTableOfContents
from .base_command import InputCommand


##############################################################################
class GeneralCommand(InputCommand):
    """Base class for general commands."""

    COMMAND = "`quit`"
    ALIASES = "`q`"
    MESSAGE: type[Message]

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
class ContentsCommand(GeneralCommand):
    """Jump to the table of contents"""

    COMMAND = "`contents`"
    ALIASES = "`c`, `toc`"
    MESSAGE = JumpToTableOfContents


##############################################################################
class QuitCommand(GeneralCommand):
    """Quit the application"""

    COMMAND = "`quit`"
    ALIASES = "`q`"
    MESSAGE = Quit


### general.py ends here
