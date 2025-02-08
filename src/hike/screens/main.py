"""The main screen for the application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import var
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.dialogs import HelpScreen
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Textual fspicker imports.
from textual_fspicker import FileOpen

##############################################################################
# Local imports.
from .. import __version__
from ..messages import OpenFile, OpenFrom, OpenURL
from ..providers import MainCommands
from ..widgets import CommandLine, Viewer


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Hike v{__version__}"

    DEFAULT_CSS = """
    Main {
        #workspace {
            border-top: blank $panel;
            border-title-align: right;
            border-title-color: $text;
            hatch: right $boost;
        }

        .panel {
            background: $surface;
            &:focus, &:focus-within {
                background: $panel 80%;
            }
        }
    }
    """

    COMMAND_MESSAGES = (
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        ChangeTheme,
        Quit,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        yield Header()
        with Horizontal(id="workspace", classes="panel"):
            yield Viewer()
        yield CommandLine(classes="panel")
        yield Footer()

    @on(Viewer.Loaded)
    def new_location(self, message: Viewer.Loaded) -> None:
        """Handle movement to a new location.

        Args:
            message: The message to handle.
        """
        self.query_one("#workspace").border_title = str(message.viewer.location or "")

    @on(OpenFile)
    @on(OpenURL)
    def open_markdown(self, message: OpenFile | OpenURL) -> None:
        """Open a file for viewing.

        Args:
            message: The message requesting the file be opened.
        """
        self.query_one(Viewer).location = message.to_open

    @on(OpenFrom)
    @work
    async def browse_for_file(self, message: OpenFrom) -> None:
        """Browse for a markdown file with a file open dialog.

        Args:
            message: The message requesting the operation.
        """
        if chosen := await self.app.push_screen_wait(FileOpen(message.location)):
            self.post_message(OpenFile(chosen))

    @on(Help)
    def action_help_command(self) -> None:
        """Toggle the display of the help panel."""
        self.app.push_screen(HelpScreen(self))

    @on(Quit)
    def action_quit_command(self) -> None:
        """Quit the application."""
        self.app.exit()


### main.py ends here
