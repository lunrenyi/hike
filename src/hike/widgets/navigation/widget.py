"""Provides the navigation panel widget."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import var
from textual.widgets import Markdown, Placeholder, TabbedContent, TabPane, Tabs, Tree
from textual.widgets.markdown import MarkdownTableOfContents, TableOfContentsType

##############################################################################
# Local imports.
from ...types import HikeHistory
from .history_view import HistoryView
from .local_view import LocalView


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
        HistoryView, &:focus-within HistoryView, LocalView, &:focus-within LocalView {
            background: transparent;
        }
    }
    """

    BINDINGS = [
        ("escape", "maybe_return_to_tabs"),
        ("down", "move_into_panel"),
    ]

    dock_right: var[bool] = var(False)
    """Should the navigation dock to the right?"""

    table_of_contents: var[TableOfContentsType | None] = var(None)
    """The currently-displayed table of contents."""

    def action_return_to_tabs(self) -> None:
        """Return focus to the tabs."""
        self.query_one(Tabs).focus()

    def action_move_into_panel(self) -> None:
        """Drop focus down into a panel."""
        if (active := self.query_one(TabbedContent).active_pane) is not None:
            active.query_one("*").focus()

    def _watch_dock_right(self) -> None:
        """React to the dock toggle being changed."""
        self.set_class(self.dock_right, "--dock-right")

    def _watch_table_of_contents(self) -> None:
        """React to the table of content being updated."""
        self.query_one(
            MarkdownTableOfContents
        ).table_of_contents = self.table_of_contents
        tabs = self.query_one(TabbedContent)
        if self.table_of_contents:
            self.query_one("MarkdownTableOfContents Tree", Tree).cursor_line = 0
            tabs.enable_tab("content")
        else:
            tabs.disable_tab("content")
            if tabs.active == "content":
                tabs.active = "local"

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        with TabbedContent():
            with TabPane("Content", id="content"):
                yield MarkdownTableOfContents(Markdown())
            with TabPane("Local", id="local"):
                yield LocalView(Path("~").expanduser())
            with TabPane("Bookmarks", id="bookmarks"):
                yield Placeholder()
            with TabPane("History", id="history"):
                yield HistoryView()

    def update_history(self, history: HikeHistory) -> None:
        """Update the history display.

        Args:
            history: The history to display.
        """
        self.query_one(HistoryView).update(history)
        tabs = self.query_one(TabbedContent)
        if history:
            tabs.enable_tab("history")
        else:
            tabs.disable_tab("history")
            if tabs.active == "history":
                tabs.active = "local"

    def highlight_history(self, history: int) -> None:
        """Highlight a specific entry in history.

        Args:
            The ID of the item of history to highlight.
        """
        self.query_one(HistoryView).highlight_location(history)


### navigation.py ends here
