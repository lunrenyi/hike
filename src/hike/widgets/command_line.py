"""A command line for getting input from the user."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Label


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


### command_line.py ends here
