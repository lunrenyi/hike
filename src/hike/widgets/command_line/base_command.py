"""Provides the base command class."""

##############################################################################
# Textual imports.
from textual.widget import Widget


##############################################################################
class InputCommand:
    """Base class for input commands."""

    COMMAND = ""
    """The command for the help."""

    ALIASES = ""
    """Any aliases for the command for the help."""

    ARGUMENTS = ""
    """Any arguments for the command for the help."""

    @classmethod
    def help_text(cls) -> str:
        """Get the help text for the command.

        Returns:
            The help text formatted as a Markdown table row.
        """
        return f"| {cls.COMMAND} | {cls.ALIASES} | {cls.ARGUMENTS} | {cls.__doc__} |"

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
