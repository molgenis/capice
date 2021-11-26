import logging
import unittest

from src.main.python.utilities.custom_logging_filter import CustomLoggingFilter


class TestCustomLoggingFilter(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print('Setting up.')
        cls.custom_filter = CustomLoggingFilter({})

    def test_filter_true(self):
        logger = logging.getLogger('simple_example')
        record = logger.makeRecord('simple_example', 3, '', 5, 'message', ('arg'), None)
        self.custom_filter.custom_loglevels = [3, 4]
        actual = self.custom_filter.filter(record)
        self.assertEqual(True, actual)

    def test_filter_false(self):
        logger = logging.getLogger('simple_example')
        record = logger.makeRecord('simple_example', 2, '', 5, 'message', ('arg'), None)
        self.custom_filter.custom_loglevels = [3, 4]
        actual = self.custom_filter.filter(record)
        self.assertEqual(False, actual)


if __name__ == '__main__':
    unittest.main()
