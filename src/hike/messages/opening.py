"""Messages to do with opening things."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from pathlib import Path

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


### opening.py ends here
