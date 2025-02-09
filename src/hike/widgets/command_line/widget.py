"""Provides a widget for getting input from the user."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Label

##############################################################################
# Local imports.
from .open_directory import OpenDirectoryCommand
from .open_file import OpenFileCommand
from .open_url import OpenURLCommand


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
        for candidate in (OpenDirectoryCommand, OpenFileCommand, OpenURLCommand):
            if candidate.handle(message.value, self):
                message.input.value = ""
                return
        self.notify("Unable to handle that input", title="Error", severity="error")


### widget.py ends here
