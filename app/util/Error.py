class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ConfigError(Error):
    """Exception raised for errors when config option could not be found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
