"""A command line for getting input from the user."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Input, Label

##############################################################################
# Local imports.
from ..messages import OpenFile, OpenFrom, OpenURL


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


##############################################################################
class OpenDirectoryCommand(InputCommand):
    """Input command for browsing for a file in a directory."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if (path := Path(text).expanduser()).is_dir():
            for_widget.post_message(OpenFrom(path))
            return True
        return False


##############################################################################
class OpenFileCommand(InputCommand):
    """Input command for opening a file."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if (path := Path(text).expanduser()).is_file():
            for_widget.post_message(OpenFile(path))
            return True
        return False


##############################################################################
class OpenURLCommand(InputCommand):
    """Input command for opening a URL."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if (url := URL(text)).is_absolute_url and url.scheme in ("http", "https"):
            for_widget.post_message(OpenURL(url))
            return True
        return False


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


### command_line.py ends here
