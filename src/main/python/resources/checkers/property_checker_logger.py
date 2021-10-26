from src.main.python.resources.checkers.property_checker import PropertyChecker
from src.main.python.core.logger import Logger


class PropertyCheckerLogger(PropertyChecker):
    """
    Same as parent PropertyChecker,
    but logs the Error raised in PropertyChecker to loglevel CRITICAL.
    """
    def __init__(self):
        super().__init__()
        self.log = Logger().logger

    def _talk_to_logger(self, msg, *args, **kwargs):
        self.log.critical(msg, *args, **kwargs)
