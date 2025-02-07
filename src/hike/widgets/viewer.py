"""Provides the Markdown viewer widget."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import var
from textual.widgets import Markdown


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

    source: var[str | Path | None] = var(None)
    """The source of the markdown being displayed."""

    def compose(self) -> ComposeResult:
        """Compose the content of the viewer."""
        yield Markdown()

    def watch_source(self) -> None:
        """Handle changes to the markdown to view."""
        self.can_focus = self.source is not None
        self.set_class(self.source is None, "empty")
        markdown = ""
        if self.source is not None:
            try:
                markdown = Path(self.source).read_text(encoding="utf-8")
            except OSError as error:
                self.notify(str(error), title="Load error", severity="error")
        self.query_one(Markdown).update(markdown)


### viewer.py ends here
