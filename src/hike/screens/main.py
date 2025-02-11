"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Markdown

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Textual fspicker imports.
from textual_fspicker import FileOpen

##############################################################################
# Local imports.
from .. import __version__
from ..commands import (
    Backward,
    ChangeNavigationSide,
    Forward,
    JumpToCommandLine,
    ToggleNavigation,
)
from ..data import load_configuration, load_history, save_history, update_configuration
from ..messages import (
    ClearHistory,
    OpenFrom,
    OpenFromHistory,
    OpenLocation,
    RemoveHistoryEntry,
    SetLocalViewRoot,
)
from ..providers import MainCommands
from ..support import maybe_markdown, view_in_browser
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
                border-left: solid $panel;
                &:focus, &:focus-within {
                    border-left: solid $border;
                }
            }
        }

        .panel {
            background: $surface;
            &:focus, &:focus-within {
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

    HELP = """
    ## Main application keys and commands

    The following key bindings and commands are available:
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
        JumpToCommandLine,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    AUTO_FOCUS = "CommandLine Input"

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
        self.query_one(Viewer).history = load_history()

    @on(OpenLocation)
    def _open_markdown(self, message: OpenLocation) -> None:
        """Open a file for viewing.

        Args:
            message: The message requesting the file be opened.
        """
        if maybe_markdown(message.to_open):
            self.query_one(Viewer).location = message.to_open
        else:
            view_in_browser(message.to_open)

    @on(OpenFrom)
    @work
    async def _browse_for_file(self, message: OpenFrom) -> None:
        """Browse for a markdown file with a file open dialog.

        Args:
            message: The message requesting the operation.
        """
        if chosen := await self.app.push_screen_wait(FileOpen(message.location)):
            self.post_message(OpenLocation(chosen))

    @on(OpenFromHistory)
    def _open_from_history(self, message: OpenFromHistory) -> None:
        """Open a location from the history.

        Args:
            message: The message requesting the history open.
        """
        self.query_one(Viewer).goto(message.location)

    @on(RemoveHistoryEntry)
    def _remove_location_from_history(self, message: RemoveHistoryEntry) -> None:
        """Remove a specific location from history.

        Args:
            message: The message requesting the location be removed.
        """
        self.query_one(Viewer).remove_from_history(message.location)

    @on(ClearHistory)
    def _clear_down_history(self) -> None:
        """Clear all items from history."""
        self.query_one(Viewer).clear_history()

    @on(SetLocalViewRoot)
    def _set_local_root(self, message: SetLocalViewRoot) -> None:
        """Change the root directory of the local file browser.

        Args:
            message: The message requesting the root be changed.
        """
        self.query_one(Navigation).set_local_view_root(message.root)

    @on(Markdown.TableOfContentsUpdated)
    def _update_navigation_contents(
        self, message: Markdown.TableOfContentsUpdated
    ) -> None:
        """Handle the table of contents being updated.

        Args:
            message: The message broadcasting that the ToC is updated.
        """
        self.query_one(Navigation).table_of_contents = message.table_of_contents

    @on(Markdown.TableOfContentsSelected)
    def _jump_to_content(self, message: Markdown.TableOfContentsSelected) -> None:
        """Jump to a specific location in the current document.

        Args:
            message: The message request the jump.
        """
        self.query_one(Viewer).jump_to_content(message.block_id)

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

    @on(JumpToCommandLine)
    def action_jump_to_command_line_command(self) -> None:
        """Jump to the command line."""
        if self.AUTO_FOCUS:
            self.query_one(self.AUTO_FOCUS).focus()

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
        save_history(message.viewer.history)

    @on(Viewer.HistoryVisit)
    def _move_history(self, message: Viewer.HistoryVisit) -> None:
        """React to a new location in history being visited."""
        if (location := message.viewer.history.current_location) is not None:
            self.query_one(Navigation).highlight_history(location)


### main.py ends here
