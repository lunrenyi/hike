"""Commands related to navigation."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class Forward(Command):
    """Move forward through history"""

    BINDING_KEY = "ctrl+right_square_bracket"


##############################################################################
class Backward(Command):
    """Move backward through history"""

    BINDING_KEY = "ctrl+left_square_bracket"


### navigation.py ends here
