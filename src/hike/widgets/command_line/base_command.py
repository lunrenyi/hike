"""Provides the base command class."""

##############################################################################
# Textual imports.
from textual.widget import Widget


##############################################################################
class InputCommand:
    """Base class for input commands."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        return False


### base_command.py ends here
