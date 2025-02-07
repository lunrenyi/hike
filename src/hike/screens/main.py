"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command, Help, Quit
from textual_enhanced.dialogs import HelpScreen
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Textual fspicker imports.
from textual_fspicker import FileOpen

##############################################################################
# Local imports.
from .. import __version__
from ..messages import OpenFile, OpenFrom
from ..providers import MainCommands
from ..widgets import CommandLine


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Hike v{__version__}"

    DEFAULT_CSS = """
    Main {
        #workspace {
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
        Quit,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)

    COMMANDS = {MainCommands}

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        yield Header()
        yield Horizontal(id="workspace", classes="panel")
        yield CommandLine(classes="panel")
        yield Footer()

    @on(OpenFile)
    def open_file(self, message: OpenFile) -> None:
        """Open a file for viewing.

        Args:
            message: The message requesting the file be opened.
        """
        self.notify(str(message.to_open))

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
