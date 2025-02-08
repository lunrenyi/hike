"""Provides the Markdown viewer widget."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import singledispatchmethod
from pathlib import Path
from typing import Callable, Final

##############################################################################
# httpx imports.
from httpx import URL, AsyncClient, HTTPStatusError, RequestError

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import var
from textual.widgets import Markdown

##############################################################################
# Local imports.
from .. import __version__
from ..support import History


##############################################################################
class Viewer(VerticalScroll):
    """The Markdown viewer widget."""

    DEFAULT_CSS = """
    Viewer {
        display: block;
        &.empty {
            display: none;
        }
        Markdown {
            background: transparent;
        }
    }
    """

    USER_AGENT: Final[str] = f"Hike v{__version__} (https://github.com/davep/hike)"
    """The user agent string for the viewer."""

    location: var[Path | URL | None] = var(None)
    """The location of the markdown being displayed."""

    def __init__(
        self,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """Initialise the viewer widget.

        Args:
            id: The ID of the widget description in the DOM.
            classes: The CSS classes of the widget description.
        """
        super().__init__(
            id=id,
            classes=classes,
        )
        self._history = History[Path | URL | None]()
        """The history for the viewer."""

    def compose(self) -> ComposeResult:
        """Compose the content of the viewer."""
        yield Markdown()

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
                    headers={"user-agent": self.USER_AGENT},
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

    def _visit(self, location: Path | URL | None, remember: bool = True) -> None:
        """Visit the given location.

        Args:
            location: The location to visit.
            remember: Should this location go into history?
        """
        self.can_focus = location is not None
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
        self.query_one(Markdown).update(message.markdown)
        if message.remember and self.location != self._history.current_item:
            self._history += self.location
            self.post_message(self.HistoryUpdated(self))

    def _move(self, movement: Callable[[], bool]) -> None:
        """Move in the given direction through history.

        Args:
            movement: The function that performs the movement.
        """
        if movement():
            self.set_reactive(Viewer.location, self._history.current_item)
            self._visit(self.location, remember=False)

    def backward(self) -> None:
        """Go backward through the history."""
        self._move(self._history.backward)

    def forward(self) -> None:
        """Go forward through the history."""
        self._move(self._history.forward)


### viewer.py ends here
