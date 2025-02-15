"""Command palette provider for the editor."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import (
    ChangeTheme,
    CommandHits,
    CommandsProvider,
    Help,
)

##############################################################################
# Local imports.
from ..commands.editor import Close, Save


##############################################################################
class EditorCommands(CommandsProvider):
    """Provides the commands for the fallback editor."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield ChangeTheme()
        yield Help()
        yield Save()
        yield Close()


### editor.py ends here
