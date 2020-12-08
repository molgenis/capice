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
