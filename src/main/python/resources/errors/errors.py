class VersionError(Exception):
    """
    Raised when a version mismatch happens
    """
    pass


class InputError(Exception):
    """
    Raised when an input argument is incorrect.
    """
    pass


class ParserError(Exception):
    """
    Raised when a Parser is unable to parse
    """
    pass


class InitializationError(Exception):
    """
    Raised when a function is called before the class is initialized
    """
    pass


class InvalidInputFileError(Exception):
    """
    Raised when an input file is given but CAPICE does not recognize its origin
    """
    pass
