"""Provides the command for opening from a URL."""

##############################################################################
# httpx imports.
from httpx import URL

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenURL
from .base_command import InputCommand


##############################################################################
class OpenURLCommand(InputCommand):
    """Input command for opening a URL."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if (url := URL(text)).is_absolute_url and url.scheme in ("http", "https"):
            for_widget.post_message(OpenURL(url))
            return True
        return False


### open_url.py ends here
