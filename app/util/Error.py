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

class FunctionNotFoundError(Error):
    """Exception raised for not registered but needed functions.

    Attributes:
        function -- the function not found
        message -- a short explanation
    """

    def __init__(self, function, message):
        self.function = function
        self.message = message

class UnsupportedModeError(Error):
    """Exception raised when trying to use an unsupported trading mode.

    Attributes:
        mode -- the unsupported mode
        message -- a short explanation
    """

    def __init__(self, mode, message):
        self.mode = mode
        self.message = message
