from src.main.python.core.logger import Logger


class PropertyChecker:
    def __init__(self):
        self.log = Logger().logger

    def check_property(self, value: any, expected_type: any):
        """
        Logger method to raise a TypeError when a Property is not set correctly.

        :param value: value to be checked
        :param expected_type: type the value should match
        """
        if not isinstance(value, expected_type):
            error_message = 'Expected variable type {} but got {}'.format(expected_type, type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
