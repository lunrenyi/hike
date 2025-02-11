"""Main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class ToggleNavigation(Command):
    """Show/hide the navigation panel"""

    BINDING_KEY = "f2"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "Nav"


##############################################################################
class ChangeNavigationSide(Command):
    """Change which side the navigation panel lives on"""

    BINDING_KEY = "shift+f2"


##############################################################################
class JumpToCommandLine(Command):
    """Jump to the command line"""

    BINDING_KEY = "/"


### navigation.py ends here
