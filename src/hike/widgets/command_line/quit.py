"""Provides the command for quitting the application."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Quit

##############################################################################
# Local imports.
from .base_command import InputCommand


##############################################################################
class QuitCommand(InputCommand):
    """Quit the application"""

    COMMAND = "`quit`"
    ALIASES = "`q`"

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if f"`{text.strip().lower()}`" in (cls.COMMAND, cls.ALIASES):
            for_widget.post_message(Quit())
            return True
        return False


### quit.py ends here
