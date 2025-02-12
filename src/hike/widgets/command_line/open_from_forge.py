"""Provides the command for opening a file from a forge."""

##############################################################################
# Python imports.
from re import Pattern, compile
from typing import Final

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenFromForge
from ...types import Forge
from .base_command import InputCommand

##############################################################################
ALIASES: Final[dict[str, Forge]] = {
    "bb": "bitbucket",
    "cb": "codeberg",
    "gh": "github",
    "gl": "gitlab",
}
"""Aliases for the forges."""


##############################################################################
class OpenFromForgeCommand(InputCommand):
    """Base class for commands that open a file from a forge."""

    ARGUMENTS = "`<owner> <repo>[:<branch>] [<file>]`"

    WITHOUT_BRANCH: Final[Pattern[str]] = compile(
        r"^(?P<owner>[^/ ]+)[/ ](?P<repo>[^ :]+)(?: +(?P<file>[^ ]+))?$"
    )
    """Regular expression for finding forge details without a branch."""

    WITH_BRANCH: Final[Pattern[str]] = compile(
        r"^(?P<owner>[^/ ]+)[/ ](?P<repo>[^ :]+):(?P<branch>[^ ]+)(?: +(?P<file>[^ ]+))?$"
    )
    """Regular expression for finding forge details with a branch."""

    FORGE: Forge = "github"
    """The forge to open from."""

    @staticmethod
    def split_command(text: str) -> tuple[str, str]:
        """Split the command for further testing.

        Args:
            text: The text of the command.

        Returns:
            The command and its arguments.
        """
        if len(candidate := text.split(maxsplit=1)) == 1:
            return candidate[0], ""
        return (candidate[0], candidate[1]) if candidate else ("", "")

    @staticmethod
    def for_forge(command: str, forge: Forge) -> bool:
        """Is the given command for the given forge?

        Args:
            command: The command to test.
            forge: The desired forge.
        """
        return ALIASES.get(command, command) == forge

    @classmethod
    def maybe_request(cls, forge: Forge, arguments: str, for_widget: Widget) -> bool:
        """Maybe request a file be opened from the given forge.

        Args:
            forge: The forge to request from.
            arguments: The arguments to parse.
            for_widget: The widget to send the request to.

        Returns:
            `True` if the arguments could be parsed, `False` if not.
        """
        if details := cls.WITHOUT_BRANCH.match(arguments):
            for_widget.post_message(
                OpenFromForge(
                    forge, details["owner"], details["repo"], filename=details["file"]
                )
            )
            return True
        if details := cls.WITH_BRANCH.match(arguments):
            for_widget.post_message(
                OpenFromForge(
                    forge,
                    details["owner"],
                    details["repo"],
                    details["branch"],
                    details["file"],
                )
            )
            return True
        return False

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the forge command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        command, arguments = cls.split_command(text)
        if cls.for_forge(command, cls.FORGE):
            return cls.maybe_request(cls.FORGE, arguments, for_widget)
        return False


##############################################################################
class OpenFromBitbucket(OpenFromForgeCommand):
    """Open a file from Bitbucket"""

    COMMAND = "`bitbucket`"
    ALIASES = "`bb`"
    FORGE = "bitbucket"


##############################################################################
class OpenFromCodeberg(OpenFromForgeCommand):
    """Open a file from BitBucket"""

    COMMAND = "`codeberg`"
    ALIASES = "`cb`"
    FORGE = "codeberg"


##############################################################################
class OpenFromGitHub(OpenFromForgeCommand):
    """Open a file from GitHub"""

    COMMAND = "`github`"
    ALIASES = "`gh`"
    FORGE = "github"


##############################################################################
class OpenFromGitLab(OpenFromForgeCommand):
    """Open a file from GitHub"""

    COMMAND = "`gitlab`"
    ALIASES = "`gl`"
    FORGE = "gitlab"


### open_from_forge.py ends here
