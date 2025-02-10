"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal
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
from ..commands import Backward, ChangeNavigationSide, Forward, ToggleNavigation
from ..data import load_configuration, update_configuration
from ..messages import OpenFrom, OpenLocation
from ..providers import MainCommands
from ..widgets import CommandLine, Navigation, Viewer


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Hike v{__version__}"

    DEFAULT_CSS = """
    Main {
        #workspace {
            hatch: right $surface;
            .panel {
                border-left: wide $panel;
                &:focus, &:focus-within {
                    border-left: wide $border;
                }
            }
        }

        .panel {
            background: $surface;
            &:focus {
                background: $panel 80%;
            }
        }

        Navigation {
            display: none;
        }
        &.navigation Navigation {
            display: block;
        }
    }
    """

    COMMAND_MESSAGES = (
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        ToggleNavigation,
        ChangeTheme,
        Quit,
        # Everything else.
        ChangeNavigationSide,
        Backward,
        Forward,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    AUTO_FOCUS = "CommandLine *"

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        yield Header()
        with Horizontal(id="workspace"):
            yield Navigation(classes="panel")
            yield Viewer(classes="panel")
        yield CommandLine(classes="panel")
        yield Footer()

    def on_mount(self) -> None:
        """Configure the screen once the DOM is mounted."""
        config = load_configuration()
        self.set_class(config.navigation_visible, "navigation")
        self.query_one(Navigation).dock_right = config.navigation_on_right

    @on(OpenLocation)
    def open_markdown(self, message: OpenLocation) -> None:
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
            self.post_message(OpenLocation(chosen))

    @on(Help)
    def action_help_command(self) -> None:
        """Toggle the display of the help panel."""
        self.app.push_screen(HelpScreen(self))

    @on(ToggleNavigation)
    def action_toggle_navigation_command(self) -> None:
        """Toggle the display of the navigation panel."""
        self.toggle_class("navigation")
        with update_configuration() as config:
            config.navigation_visible = self.has_class("navigation")

    @on(ChangeNavigationSide)
    def action_change_navigation_side_command(self) -> None:
        """Change the side that the navigation panel lives on."""
        navigation = self.query_one(Navigation)
        navigation.dock_right = not navigation.dock_right
        with update_configuration() as config:
            config.navigation_on_right = navigation.dock_right

    @on(Quit)
    def action_quit_command(self) -> None:
        """Quit the application."""
        self.app.exit()

    @on(Backward)
    def action_backward_command(self) -> None:
        """Move backward through history."""
        self.query_one(Viewer).backward()

    @on(Forward)
    def action_forward_command(self) -> None:
        """Move forward through history."""
        self.query_one(Viewer).forward()

    @on(Viewer.HistoryUpdated)
    def _update_history(self, message: Viewer.HistoryUpdated) -> None:
        """Update the view of history when it changes.

        Args:
            message: The message to say that history changed.
        """
        self.query_one(Navigation).update_history(message.viewer.history)


### main.py ends here
