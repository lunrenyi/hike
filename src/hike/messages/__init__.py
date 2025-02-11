"""Provides application-wide messages."""

##############################################################################
# Local imports.
from .history import RemoveHistoryEntry
from .opening import OpenFrom, OpenFromHistory, OpenLocation

##############################################################################
# Exports.
__all__ = ["OpenFrom", "OpenFromHistory", "OpenLocation", "RemoveHistoryEntry"]

### __init__.py ends here
