"""Provides a widget for getting input from the user."""

##############################################################################
# Python imports.
from typing import Final, TypeAlias

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import var
from textual.widgets import Input, Label
from textual.widgets.input import Selection

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Quit

##############################################################################
# Local imports.
from ...support import History
from .base_command import InputCommand
from .change_directory import ChangeDirectoryCommand
from .open_directory import OpenDirectoryCommand
from .open_file import OpenFileCommand
from .open_from_forge import (
    OpenFromBitbucket,
    OpenFromCodeberg,
    OpenFromGitHub,
    OpenFromGitLab,
)
from .open_url import OpenURLCommand

##############################################################################
COMMANDS: Final[tuple[type[InputCommand], ...]] = (
    # Keep the first three in order. A file match should win over a
    # directory should win over a URL.
    OpenFileCommand,
    OpenDirectoryCommand,
    OpenURLCommand,
    # Once the above are out of the way the order doesn't matter so much.
    ChangeDirectoryCommand,
    OpenFromBitbucket,
    OpenFromCodeberg,
    OpenFromGitHub,
    OpenFromGitLab,
)
"""The commands used for the input."""


##############################################################################
CommandHistory: TypeAlias = History[str]
"""Type of the command line history."""


##############################################################################
class CommandLine(Horizontal):
    """A command line for getting input from the user."""

    DEFAULT_CSS = """
    CommandLine {
        height: 1;
        Label, Input {
            color: $text-muted;
        }
        &:focus-within {
            Label, Input {
                color: $text;
            }
            Label {
                text-style: bold;
            }
        }
        Input, Input:focus {
            border: none;
            padding: 0;
            height: 1fr;
            background: transparent;
        }
    }
    """

    HELP = f"""
    ## Command Line

    Use this command line to enter filenames, directories, URLs or commands. Entering
    a filename or a URL will open that file for viewing; entering a
    directory will open a file opening dialog starting at that location.

    | Command | Aliases | Arguments | Description |
    | --      | --      | --        | --          |
    {'\n    '.join(command.help_text() for command in COMMANDS)}

    ### Forge support

    The forge-oriented commands listed above accept a number of different
    ways of quickly specifying which file you want to view. Examples include:

    | Format | Effect |
    | -- | -- |
    | `<owner>/<repo>` | Open `README.md` from a repository |
    | `<owner> <repo>` | Open `README.md` from a repository |
    | `<owner>/<repo> <file>` | Open a specific file from a repository |
    | `<owner> <repo> <file>` | Open a specific file from a repository |
    | `<owner>/<repo>:<branch>` | Open `README.md` from a specific branch of a repository |
    | `<owner> <repo>:<branch>` | Open `README.md` from a specific branch of a repository |
    | `<owner>/<repo>:<branch> <file>` | Open a specific file from a specific branch of a repository |
    | `<owner> <repo>:<branch> <file>` | Open a specific file from a specific branch of a repository |

    If `<branch>` is omitted the requested file is looked for first in the
    `main` branch and then `master`.
    """

    BINDINGS = [
        ("escape", "request_exit"),
        ("up", "history_previous"),
        ("down", "history_next"),
    ]

    _history: var[CommandHistory] = var(CommandHistory)
    """The command line history."""

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        yield Label("> ")
        yield Input(placeholder="Enter a directory, file, path or command")

    @on(Input.Submitted)
    def _handle_input(self, message: Input.Submitted) -> None:
        """Handle input from the user.

        Args:
            message: The message requesting input is handled.
        """
        message.stop()
        for candidate in COMMANDS:
            if candidate.handle(message.value, self):
                self._history.add(message.value)
                message.input.value = ""
                return
        self.notify("Unable to handle that input", title="Error", severity="error")

    def action_request_exit(self) -> None:
        """Request that the application quits."""
        self.post_message(Quit())

    def action_history_previous(self) -> None:
        """Move backwards through the command line history."""
        if value := self._history.current_item:
            self.query_one(Input).value = value
            self.query_one(Input).selection = Selection(0, len(value))
            self._history.backward()

    def action_history_next(self) -> None:
        """Move forwards through the command line history."""
        if (
            self._history.forward()
            and (value := self._history.current_item) is not None
        ):
            self.query_one(Input).value = value
            self.query_one(Input).selection = Selection(0, len(value))
        else:
            self.query_one(Input).value = ""


### widget.py ends here
