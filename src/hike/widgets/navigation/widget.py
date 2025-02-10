"""Provides the navigation panel widget."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import var
from textual.widgets import Markdown, Placeholder, TabbedContent, Tree
from textual.widgets.markdown import MarkdownTableOfContents, TableOfContentsType

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

        #tabs-list {
            background: $panel;
        }

        /* https://github.com/Textualize/textual/issues/5488 */
        MarkdownTableOfContents, &:focus-within MarkdownTableOfContents {
            background: transparent;
            width: 1fr;
            Tree {
                background: transparent;
            }
        }

        /* https://github.com/Textualize/textual/issues/5488 */
        HistoryView, &:focus-within HistoryView {
            background: transparent;
        }
    }
    """

    dock_right: var[bool] = var(False)
    """Should the navigation dock to the right?"""

    table_of_contents: var[TableOfContentsType | None] = var(None)

    _history: var[HistoryView | None] = var(None)
    """The history display."""

    def _watch_dock_right(self) -> None:
        """React to the dock toggle being changed."""
        self.set_class(self.dock_right, "--dock-right")

    def _watch_table_of_contents(self) -> None:
        """React to the table of content being updated."""
        self.query_one(
            MarkdownTableOfContents
        ).table_of_contents = self.table_of_contents
        self.query_one("MarkdownTableOfContents Tree", Tree).cursor_line = 0

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        self._history = HistoryView()
        with TabbedContent("Content", "Local", "Bookmarks", "History"):
            yield MarkdownTableOfContents(Markdown())
            yield Placeholder()
            yield Placeholder()
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
