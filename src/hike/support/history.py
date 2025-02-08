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

    def __init__(
        self, history: Sequence[HistoryItem] | None = None, max_length: int = 500
    ) -> None:
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
        """The current integer location in the history.

        If there is no valid location the value is `None`.
        """
        try:
            _ = self._history[self._current]
        except IndexError:
            return None
        return self._current

    @property
    def current_item(self) -> HistoryItem | None:
        """The current item in the history.

        If there is no current item in the history the value is `None`.
        """
        try:
            return self._history[self._current]
        except IndexError:
            return None

    def backward(self) -> bool:
        """Go backward through the history.

        Returns:
            `True` if we moved through history, `False` if not.
        """
        if self._current:
            self._current -= 1
            return True
        return False

    def forward(self) -> bool:
        """Go forward through the history.

        Returns:
            `True` if we moved through history, `False` if not.
        """
        if self._current < len(self._history) - 1:
            self._current += 1
            return True
        return False

    def __iadd__(self, item: HistoryItem) -> Self:
        """Add an item to the history."""
        self._history.append(item)
        self._current = len(self._history) - 1
        return self

    def __len__(self) -> int:
        """The length of the history."""
        return len(self._history)


### history.py ends here
