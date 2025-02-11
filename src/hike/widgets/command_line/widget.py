"""Provides a widget for getting input from the user."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Quit

##############################################################################
# Local imports.
from .base_command import InputCommand
from .open_directory import OpenDirectoryCommand
from .open_file import OpenFileCommand
from .open_url import OpenURLCommand

##############################################################################
COMMANDS: Final[tuple[type[InputCommand], ...]] = (
    OpenDirectoryCommand,
    OpenFileCommand,
    OpenURLCommand,
)
"""The commands used for the input."""


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

    Use this command line to enter filenames, directories or URLs. Entering
    a filename or a URL will open that file for viewing; entering a
    directory will open a file opening dialog starting at that location.

    | Command | Aliases | Arguments | Description |
    | --      | --      | --        | --          |
    {'\n    '.join(command.help_text() for command in COMMANDS)}
    """

    BINDINGS = [("escape", "request_exit")]

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
                message.input.value = ""
                return
        self.notify("Unable to handle that input", title="Error", severity="error")

    def action_request_exit(self) -> None:
        """Request that the application quits."""
        self.post_message(Quit())


### widget.py ends here
