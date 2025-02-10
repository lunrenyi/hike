"""Provides the history for the navigation panel."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Textual imports.
from textual import on
from textual.widgets.option_list import Option

##############################################################################
# Textual-enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ...messages import OpenLocation
from ...types import HikeHistory, HikeLocation


##############################################################################
class Location(Option):
    """A location within the history."""

    def __init__(self, location_id: int, location: HikeLocation) -> None:
        """Initialise the location object.

        Args:
            location_id: The ID of the location within the history.
            location: The location.
        """
        self.location_id = location_id
        """The ID of the location within the history."""
        self.location = location
        """The location."""
        super().__init__(
            Text.from_markup(
                f":page_facing_up: [bold]{location.name}[/]\n[dim]{location.parent}[/]",
                overflow="ellipsis",
            )
            if isinstance(location, Path)
            else Text.from_markup(
                f":globe_with_meridians: [bold]{Path(location.path).name}[/]"
                f"\n[dim]{Path(location.path).parent}\n{location.host}[/]",
                overflow="ellipsis",
            )
        )


##############################################################################
class HistoryView(EnhancedOptionList):
    """The display of history."""

    DEFAULT_CSS = """
    HistoryView {
        height: 1fr;
        border: none;
        &:focus {
            border: none;
        }
    }
    """

    def update(self, history: HikeHistory) -> None:
        """Update the content of the history view.

        Args:
            history: The history to update with.
        """
        with self.preserved_highlight:
            self.clear_options().add_options(
                Location(location_id, location)
                for location_id, location in reversed(list(enumerate(history)))
            )

    @on(EnhancedOptionList.OptionSelected)
    def visit_from_history(self, message: EnhancedOptionList.OptionSelected) -> None:
        """Visit a location from history.

        Args:
            message: The message to say which option was selected.
        """
        message.stop()
        assert isinstance(message.option, Location)
        self.post_message(OpenLocation(message.option.location))


### history.py ends here
