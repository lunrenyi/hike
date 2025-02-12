"""Messages to do with opening things."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from pathlib import Path

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ..types import Forge, HikeLocation


##############################################################################
@dataclass
class OpenFrom(Message):
    """Open a file starting at a particular location."""

    location: Path = Path(".")
    """The location to start browsing for a file."""


##############################################################################
@dataclass
class OpenLocation(Message):
    """Open a given location for viewing."""

    to_open: HikeLocation
    """The location to open."""


##############################################################################
@dataclass
class OpenFromHistory(Message):
    """Open a location found in history."""

    location: int
    """The location in the history to open."""


##############################################################################
@dataclass
class OpenFromForge(Message):
    """Open a file from a forge."""

    forge: Forge
    """The forge to open from."""

    owner: str
    """The owner of the repository to open from."""

    repository: str
    """The repository to open the file from."""

    branch: str | None = None
    """The optional branch to open from."""

    filename: str | None = None
    """The optional name of the file to open."""


### opening.py ends here
