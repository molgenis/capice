from src.main.python.resources.checkers.property_checker import PropertyChecker
import logging
logger = logging.getLogger(__name__)

class PropertyCheckerLogger(PropertyChecker):
    def __init__(self):
        super().__init__()

    def _talk_to_logger(self, error_message):
        logger.critical(error_message)
