"""Provides the navigation panel widget."""

##############################################################################
# Textual imports.
from textual.containers import Vertical
from textual.reactive import var


##############################################################################
class Navigation(Vertical):
    """The navigation panel."""

    DEFAULT_CSS = """
    Navigation {
        width: 27%;
        dock: left;
        &.--dock-right {
            dock: right;
        }
    }
    """

    dock_right: var[bool] = var(False)
    """Should the navigation dock to the right?"""

    def _watch_dock_right(self) -> None:
        """React to the dock toggle being changed."""
        self.set_class(self.dock_right, "--dock-right")


### navigation.py ends here
