"""Messages to do with opening things."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL

##############################################################################
# Textual imports.
from textual.message import Message


##############################################################################
@dataclass
class OpenFrom(Message):
    """Open a file starting at a particular location."""

    location: Path = Path(".")
    """The location to start browsing for a file."""


##############################################################################
@dataclass
class OpenFile(Message):
    """Open a given file for viewing."""

    to_open: Path
    """The file to open."""


##############################################################################
@dataclass
class OpenURL(Message):
    """Open a given URL for viewing."""

    to_open: URL
    """The URL to open."""

### opening.py ends here
