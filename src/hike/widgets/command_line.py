"""A command line for getting input from the user."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Input, Label

##############################################################################
# Local imports.
from ..messages import OpenFile, OpenFrom


##############################################################################
class InputCommand:
    """Base class for input commands."""

    @classmethod
    def can_handle(cls, text: str) -> bool:
        """Can the class handle the given input?

        Args:
            text: The text to check.
        """
        return False

    @classmethod
    def handle(self, text: str, checker: Widget) -> None:
        """Handle the command.

        Args:
            text: The text of the command.
        """


##############################################################################
class OpenDirectoryCommand(InputCommand):
    @classmethod
    def can_handle(cls, text: str) -> bool:
        """Can the class handle the given input?

        Args:
            text: The text to check.
        """
        return Path(text).is_dir()

    @classmethod
    def handle(cls, text: str, checker: Widget) -> None:
        """Handle the command.

        Args:
            text: The text of the command.
        """
        checker.post_message(OpenFrom(Path(text)))


##############################################################################
class OpenFileCommand(InputCommand):
    @classmethod
    def can_handle(cls, text: str) -> bool:
        """Can the class handle the given input?

        Args:
            text: The text to check.
        """
        return Path(text).is_file()

    @classmethod
    def handle(cls, text: str, checker: Widget) -> None:
        """Handle the command.

        Args:
            text: The text of the command.
        """
        checker.post_message(OpenFile(Path(text)))


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
        }
        Input, Input:focus {
            border: none;
            padding: 0;
            height: 1fr;
            background: transparent;
        }
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        yield Label("> ")
        yield Input()

    @on(Input.Submitted)
    def _handle_input(self, message: Input.Submitted) -> None:
        """Handle input from the user.

        Args:
            message: The message requesting input is handled.
        """
        message.stop()
        for candidate in (OpenDirectoryCommand, OpenFileCommand):
            if candidate.can_handle(message.value):
                candidate.handle(message.value, self)
                message.input.value = ""
                return
        self.notify("Unable to handle that input", title="Error", severity="error")


### command_line.py ends here
