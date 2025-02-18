"""Provides the command for jumping to the table of contents."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...commands import JumpToTableOfContents
from .base_command import InputCommand


##############################################################################
class ContentsCommand(InputCommand):
    """Quit the application"""

    COMMAND = "`contents`"
    ALIASES = "`c`, `toc`"

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
            for_widget.post_message(JumpToTableOfContents())
            return True
        return False


### contents.py ends here
