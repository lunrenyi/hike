"""Commands for the fallback editor."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class Save(Command):
    """Save changes back to the document"""

    BINDING_KEY = "f2, ctrl+s"
    SHOW_IN_FOOTER = True


##############################################################################
class Close(Command):
    """Close the editor"""

    BINDING_KEY = "f10"
    SHOW_IN_FOOTER = True


### editor.py ends here
