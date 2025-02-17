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

    @staticmethod
    def split_command(text: str) -> tuple[str, str]:
        """Split the command for further testing.

        Args:
            text: The text of the command.

        Returns:
            The command and its tail.
        """
        command, _, tail = text.strip().partition(" ")
        return command.strip(), tail.strip()

    @classmethod
    def is_command(cls, command: str) -> bool:
        """Does the given command appear to be a match?

        Args:
            command: The command to test.

        Returns:
            `True` if the given command seems to be a match, `False` if not.
        """
        # Build up all the possible matches. These are built from the main
        # command and also the aliases. By convention the code will often
        # use `code` fences for commands, and the aliases will be a comma
        # list, so we clean that up as we go...
        return command.strip().lower() in (
            candidate.strip().lower().removeprefix("`").removesuffix("`")
            for candidate in (cls.COMMAND, *cls.ALIASES.split(","))
        )


### base_command.py ends here
