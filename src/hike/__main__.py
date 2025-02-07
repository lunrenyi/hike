"""The main entry point for the application."""

##############################################################################
# Local imports.
from .hike import Hike


##############################################################################
def main() -> None:
    """The main entry point."""
    Hike().run()


##############################################################################
if __name__ == "__main__":
    main()


### __main__.py ends here
