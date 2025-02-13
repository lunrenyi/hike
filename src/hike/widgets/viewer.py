"""Provides the Markdown viewer widget."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import singledispatchmethod
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL, AsyncClient, HTTPStatusError, RequestError

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import var
from textual.widgets import Label, Markdown, Rule

##############################################################################
# Local imports.
from .. import USER_AGENT
from ..commands import JumpToCommandLine
from ..messages import OpenLocation
from ..support import looks_urllike
from ..types import HikeHistory, HikeLocation


##############################################################################
class ViewerTitle(Label):
    """Widget to display the viewer's title."""

    DEFAULT_CSS = """
    ViewerTitle {
        background: $panel;
        color: $foreground;
        content-align: right middle;
        width: 1fr;
    }
    """

    location: var[HikeLocation | None] = var(None)
    """The location to display."""

    def _watch_location(self) -> None:
        """React to the location changing."""
        self.update(str(self.location or ""))


##############################################################################
class Viewer(Vertical, can_focus=False):
    """The Markdown viewer widget."""

    DEFAULT_CSS = """
    Viewer {
        display: block;
        &.empty {
            display: none;
        }
        &> VerticalScroll {
            background: transparent;
        }
        Markdown {
            background: transparent;
        }
        Rule {
            height: 1;
            margin: 0 !important;
            color: $foreground 10%;
        }
    }
    """

    BINDINGS = [("escape", "bounce_out")]

    location: var[HikeLocation | None] = var(None)
    """The location of the markdown being displayed."""

    history: var[HikeHistory] = var(HikeHistory)
    """The history for the viewer."""

    def compose(self) -> ComposeResult:
        """Compose the content of the viewer."""
        yield ViewerTitle()
        yield Rule(line_style="heavy")
        with VerticalScroll():
            yield Markdown(open_links=False)

    def action_bounce_out(self) -> None:
        """Bounce back out to the input."""
        self.post_message(JumpToCommandLine())

    @dataclass
    class Loaded(Message):
        """Class posted when the markdown content is loaded."""

        viewer: Viewer
        """The viewer."""

        markdown: str
        """The markdown content."""

        remember: bool
        """Should this load be remembered?"""

    @dataclass
    class HistoryUpdated(Message):
        """Class posted when the history is updated."""

        viewer: Viewer
        """The viewer."""

    @dataclass
    class HistoryVisit(Message):
        """Class posted when a location in history is visited."""

        viewer: Viewer
        """The viewer."""

    @on(HistoryUpdated)
    def _history_updated(self) -> None:
        """React to the bindings being updated."""
        self.refresh_bindings()
        # Given that the content of history has changed, we need to update
        # the display. If we have history...
        if self.history:
            # ...visit whatever is now current.
            self._visit_from_history()
        else:
            # ...otherwise there's nothing to display.
            self.location = None

    def _watch_history(self) -> None:
        """React to the history being updated."""
        self.post_message(self.HistoryUpdated(self))

    @work(thread=True, exclusive=True)
    def _load_from_file(self, location: Path, remember: bool) -> None:
        """Load up markdown content from a file.

        Args:
            location: The path to load the content from.
            remember: Should this location go into history?
        """
        try:
            self.post_message(
                self.Loaded(self, Path(location).read_text(encoding="utf-8"), remember)
            )
        except OSError as error:
            self.notify(str(error), title="Load error", severity="error", timeout=8)

    @work(exclusive=True)
    async def _load_from_url(self, location: URL, remember: bool) -> None:
        """Load up markdown content from a URL.

        Args:
            location: The URL to load the content from.
            remember: Should this location go into history?
        """

        # Download the data from the remote location.
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    location,
                    follow_redirects=True,
                    headers={"user-agent": USER_AGENT},
                )
        except RequestError as error:
            self.notify(str(error), title="Request error", severity="error", timeout=8)
            return

        # We got a response, left's check it's a good one.
        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            self.notify(str(error), title="Response error", severity="error", timeout=8)
            return

        # At this point we've got a good response. Now let's be sure that
        # what we got back is something that admits to being markdown, or at
        # least a form of plain text we can render.
        if content_type := response.headers.get("content-type"):
            if any(
                content_type.startswith(f"text/{sub_type}")
                for sub_type in ("plain", "markdown", "x-markdown")
            ):
                self.post_message(self.Loaded(self, response.text, remember))
                return
        # TODO: Be kind and open the URL outwith the viewer.
        self.notify("That didn't look like markdown to me.")

    @singledispatchmethod
    def _load_markdown(self, location: Path, remember: bool) -> None:
        """Load markdown from a location.

        Args:
            location: The location to load the markdown from.
            remember: Should this location go into history?
        """
        self._load_from_file(location, remember)

    @_load_markdown.register
    def _(self, location: URL, remember: bool) -> None:
        self._load_from_url(location, remember)

    @_load_markdown.register
    def _(self, location: None, remember: bool) -> None:
        self.post_message(self.Loaded(self, "", remember))

    def _visit(self, location: HikeLocation | None, remember: bool = True) -> None:
        """Visit the given location.

        Args:
            location: The location to visit.
            remember: Should this location go into history?
        """
        self.set_class(location is None, "empty")
        self._load_markdown(location, remember)

    def _watch_location(self) -> None:
        """Handle changes to the location to view."""
        self._visit(self.location)

    @on(Loaded)
    def _update_markdown(self, message: Loaded) -> None:
        """Update the markdown once some new content is loaded.

        Args:
            message: The message requesting the update.
        """
        self.query_one(ViewerTitle).location = self.location
        self.query_one(Markdown).update(message.markdown)
        if (
            message.remember
            and self.location
            and self.location != self.history.current_item
        ):
            self.history.add(self.location)
            self.post_message(self.HistoryUpdated(self))

    def _visit_from_history(self) -> None:
        """Visit the current location in history."""
        self.set_reactive(Viewer.location, self.history.current_item)
        self._visit(self.location, remember=False)
        self.post_message(self.HistoryVisit(self))

    def reload(self) -> None:
        """Reload the current document."""
        self._visit(self.location, remember=False)

    def goto(self, history_location: int) -> None:
        """Go to a specific location in history."""
        if self.history.current_location != history_location:
            self.history.goto(history_location)
            self._visit_from_history()

    def backward(self) -> None:
        """Go backward through the history."""
        if self.history.backward():
            self._visit_from_history()

    def forward(self) -> None:
        """Go forward through the history."""
        if self.history.forward():
            self._visit_from_history()

    def jump_to_content(self, block_id: str) -> None:
        """Jump to some content in the current document.

        Args:
            block_id: The ID of the content to jump to.
        """
        self.scroll_to_widget(self.query_one(f"#{block_id}"), top=True)

    def remove_from_history(self, history: int) -> None:
        """Remove a specific location from history.

        Args:
            history: The ID of the location in history to remove.
        """
        del self.history[history]
        self.post_message(self.HistoryUpdated(self))

    def clear_history(self) -> None:
        """Clear all locations from history."""
        self.history = HikeHistory()

    @on(Markdown.LinkClicked)
    def _handle_link(self, message: Markdown.LinkClicked) -> None:
        """Handle a link being clicked in the Markdown widget.

        Args:
            message: The message requesting the link be handled.
        """
        message.stop()

        # Outright URL?
        if looks_urllike(message.href):
            self.post_message(OpenLocation(URL(message.href)))
            return

        # Possibly a relative path to a currently-visited URL?
        if isinstance(self.location, URL):
            self.post_message(
                OpenLocation(self.location.copy_with().join(message.href))
            )
            return

        # A local file that exists?
        if (local_file := Path(message.href).expanduser()).exists():
            self.post_message(OpenLocation(local_file.resolve()))
            return

        # A local file relative to the current location?
        if (
            isinstance(self.location, Path)
            and (local_file := self.location / Path(message.href)).absolute().exists()
        ):
            self.post_message(OpenLocation(local_file))
            return

        # Some sort of internal anchor perhaps?
        if message.href.startswith("#") and message.markdown.goto_anchor(
            message.href[1:]
        ):
            return

        self.notify(
            f"The clicked link could not be handled:\n\n{message.href}",
            title="Unknown link type",
            severity="error",
        )


### viewer.py ends here
