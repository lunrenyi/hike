"""Provides the main application commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import (
    ChangeTheme,
    CommandHits,
    CommandsProvider,
    Help,
    Quit,
)

##############################################################################
# Local imports.
from ..commands import (
    Backward,
    BookmarkLocation,
    ChangeNavigationSide,
    Forward,
    JumpToCommandLine,
    Reload,
    ToggleNavigation,
)


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield Backward()
        yield BookmarkLocation()
        yield ChangeNavigationSide()
        yield ChangeTheme()
        yield Forward()
        yield Help()
        yield JumpToCommandLine()
        yield Quit()
        yield Reload()
        yield ToggleNavigation()


### main.py ends here
