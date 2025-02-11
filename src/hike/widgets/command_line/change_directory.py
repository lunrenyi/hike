"""Provides a command for changing the directory of the local file viewer."""

##############################################################################
# Python imports.
from pathlib import Path
from re import Pattern, compile
from typing import Final

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import SetLocalViewRoot
from .base_command import InputCommand

##############################################################################
CHDIR: Final[Pattern[str]] = compile(r"^\s*(chdir|cd)\s+(?P<directory>\S+)\s*$")
"""Regular expression for matching the command."""


##############################################################################
class ChangeDirectoryCommand(InputCommand):
    """Change the root directory of the local file browser"""

    COMMAND = "`chdir`"
    ALIASES = "`cd`"
    ARGUMENTS = "`<directory>`"

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if match := CHDIR.search(text):
            if (root := Path(match["directory"]).expanduser()).is_dir():
                for_widget.post_message(SetLocalViewRoot(Path(root).resolve()))
                return True
        return False


### change_directory.py ends here
