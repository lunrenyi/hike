"""Provides the navigation panel widget."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import var

##############################################################################
# Local imports.
from ...types import HikeHistory
from .history_view import HistoryView


##############################################################################
class Navigation(Vertical):
    """The navigation panel."""

    DEFAULT_CSS = """
    Navigation {
        width: 27%;
        dock: left;
        background: transparent;
        &.--dock-right {
            dock: right;
        }
    }
    """

    dock_right: var[bool] = var(False)
    """Should the navigation dock to the right?"""

    _history: var[HistoryView | None] = var(None)
    """The history display."""

    def _watch_dock_right(self) -> None:
        """React to the dock toggle being changed."""
        self.set_class(self.dock_right, "--dock-right")

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        self._history = HistoryView()
        yield self._history

    def update_history(self, history: HikeHistory) -> None:
        """Update the history display.

        Args:
            history: The history to display.
        """
        if self._history:
            self._history.update(history)

    def highlight_history(self, history: int) -> None:
        """Highlight a specific entry in history.

        Args:
            The ID of the item of history to highlight.
        """
        if self._history:
            self._history.highlight_location(history)


### navigation.py ends here
