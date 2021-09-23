from src.main.python.resources.checkers.property_checker import PropertyChecker
from src.main.python.core.logger import Logger


class PropertyCheckerLogger(PropertyChecker):
    def __init__(self):
        super().__init__()
        self.log = Logger().logger

    def _talk_to_logger(self, error_message):
        self.log.critical(error_message)
