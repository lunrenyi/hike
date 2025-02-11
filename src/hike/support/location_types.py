"""Functions for testing location types."""

##############################################################################
# Python imports.
from functools import singledispatch
from pathlib import Path

##############################################################################
# httpx imports.
from httpx import URL


##############################################################################
@singledispatch
def maybe_markdown(location: object) -> bool:
    """Does the given location look like it might be a Markdown file?

    Args:
        location: The location to test.

    Returns:
        `True` if the location looks like it's Markdown, `False` if not.
    """
    return False


##############################################################################
@maybe_markdown.register
def _(location: Path) -> bool:
    return location.suffix.lower() in (".md", ".markdown")


##############################################################################
@maybe_markdown.register
def _(location: str) -> bool:
    return maybe_markdown(Path(location))


##############################################################################
@maybe_markdown.register
def _(location: URL) -> bool:
    return maybe_markdown(location.path)


### location_types.py ends here
