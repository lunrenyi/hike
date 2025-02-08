"""Provides the Markdown viewer widget."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import singledispatchmethod
from pathlib import Path
from typing import Final

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

    source: var[Path | URL | None] = var(None)
    """The source of the markdown being displayed."""

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

    @work(thread=True, exclusive=True)
    def _load_from_file(self, source: Path) -> None:
        """Load up markdown content from a file.

        Args:
            source: The path to load the content from.
        """
        try:
            self.post_message(
                self.Loaded(self, Path(source).read_text(encoding="utf-8"))
            )
        except OSError as error:
            self.notify(str(error), title="Load error", severity="error", timeout=8)

    @work(exclusive=True)
    async def _load_from_url(self, source: URL) -> None:
        """Load up markdown content from a URL.

        Args:
            source: The URL to load the content from.
        """

        # Download the data from the remote location.
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    source,
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
                self.post_message(self.Loaded(self, response.text))
                return
        # TODO: Be kind and open the URL outwith the viewer.
        self.notify("That didn't look like markdown to me.")

    @singledispatchmethod
    def _load_markdown(self, source: Path) -> None:
        """Load markdown from a source.

        Args:
            source: The source to load the markdown from.
        """
        self._load_from_file(source)

    @_load_markdown.register
    def _(self, source: URL) -> None:
        self._load_from_url(source)

    @_load_markdown.register
    def _(self, source: None) -> None:
        self.post_message(self.Loaded(self, ""))

    def watch_source(self) -> None:
        """Handle changes to the markdown to view."""
        self.can_focus = self.source is not None
        self.set_class(self.source is None, "empty")
        self._load_markdown(self.source)

    @on(Loaded)
    def _update_markdown(self, message: Loaded):
        """Update the markdown once some new content is loaded.

        Args:
            message: The message requesting the update.
        """
        self.query_one(Markdown).update(message.markdown)


### viewer.py ends here
