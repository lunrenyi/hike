"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command, Help, Quit
from textual_enhanced.dialogs import HelpScreen
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Local imports.
from ..providers import MainCommands


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

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
        yield Footer()

    @on(Help)
    def action_help_command(self) -> None:
        """Toggle the display of the help panel."""
        self.app.push_screen(HelpScreen(self))

    @on(Quit)
    def action_quit_command(self) -> None:
        """Quit the application."""
        self.app.exit()


### main.py ends here
