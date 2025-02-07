"""Provides the Markdown viewer widget."""

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

    markdown: var[str] = var("")
    """The markdown to view."""

    def compose(self) -> ComposeResult:
        """Compose the content of the viewer."""
        yield Markdown()

    def watch_markdown(self) -> None:
        """Handle changes to the markdown to view."""
        self.can_focus = bool(self.markdown)
        self.set_class(not self.can_focus, "empty")
        self.query_one(Markdown).update(self.markdown)


### viewer.py ends here
