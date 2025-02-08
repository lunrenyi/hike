"""Provides a history tracking class."""

##############################################################################
# Python imports.
from collections import deque
from typing import Generic, Sequence, TypeVar

##############################################################################
# Typing extensions imports.
from typing_extensions import Self

##############################################################################
HistoryItem = TypeVar("HistoryItem")
"""The type of an item in history."""

##############################################################################
class History(Generic[HistoryItem]):
    """A class for handling and tracking history."""

    def __init__(self, history: Sequence[HistoryItem] | None = None, max_length: int=500) -> None:
        """Initialise the history object.

        Args:
            history: Set to the given history.
            max_length: Optional maximum length for the history.
        """
        self._history: deque[HistoryItem] = deque(history or [], maxlen=max_length)
        """The history."""
        self._current = max(len(self._history) - 1, 0)
        """The current location within the history."""

    @property
    def current_location(self) -> int | None:
        """The current location in the history."""
        try:
           _ = self._history[self._current]
        except IndexError:
            return None
        return self._current

    @property
    def current_item(self) -> HistoryItem | None:
        """The current item in the history."""
        try:
            return self._history[self._current]
        except IndexError:
            return None

    def __iadd__(self, item: HistoryItem) -> Self:
        self._history.append(item)
        self._current = len(self._history) - 1
        return self

    def __len__(self) -> int:
        """The length of the history."""
        return len(self._history)

### history.py ends here
