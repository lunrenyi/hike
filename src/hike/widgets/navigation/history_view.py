"""Provides the history for the navigation panel."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL

##############################################################################
# Textual-enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ...support import History


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

    def update(self, history: History[Path | URL | None]) -> None:
        """Update the content of the history view.

        Args:
            history: The history to update with.
        """
        with self.preserved_highlight:
            self.clear_options().add_options(str(item) for item in history)


### history.py ends here
