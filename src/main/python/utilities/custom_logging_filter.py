import logging


class CustomLoggingFilter(logging.Filter):
    """
    Custom logging filter class to make sure that stdout only contains
    INFO or DEBUG calls.
    """
    def __init__(self, custom_loglevels):
        """
        :param custom_loglevels: str or iterable: the loglevels that should pass
        this logging filter.
        """
        super(CustomLoggingFilter, self).__init__()
        self.custom_loglevels = custom_loglevels

    def filter(self, record) -> bool:
        return record.levelno in self.custom_loglevels
