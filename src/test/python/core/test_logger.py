import sys
import unittest
from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.test.python.test_templates import teardown
import io


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager = CapiceManager()
        cls.manager.critical_logging_only = False

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    @staticmethod
    def capture_stdout_call():
        old_stdout = sys.stdout
        listener = io.StringIO()
        sys.stdout = listener
        log = Logger().logger
        log.info('SomeString')
        log.debug('SomeString')
        out = listener.getvalue()
        sys.stdout = old_stdout
        return out

    @staticmethod
    def capture_stderr_call():
        old_stderr = sys.stderr
        listener = io.StringIO()
        sys.stderr = listener
        log = Logger().logger
        log.critical('SomeString')
        log.error('SomeString')
        out = listener.getvalue()
        sys.stderr = old_stderr
        return out

    def setUp(self):
        print('Testing case:')

    def tearDown(self) -> None:
        print('Resetting arguments.')
        Logger.instance = None
        self.manager.critical_logging_only = False
        self.manager.loglevel = None

    def test_loglevel_nonverbose(self):
        """
        Testing Info messages just became a lot harder since the logger is set
        to logging.NOTSET by default, with it's StreamHandlers taking care of
        the messages itself, specially the stdout StreamHandler.
        """
        print('Loglevel info')
        self.manager.loglevel = 20  # 20 = logging.INFO
        out = self.capture_stdout_call()
        self.assertIn('INFO', out)
        self.assertNotIn('DEBUG', out)

    def test_loglevel_verbose(self):
        print('Loglevel verbose')
        self.manager.loglevel = 10  # 10 = logging.DEBUG
        out = self.capture_stdout_call()
        self.assertIn('INFO', out)
        self.assertIn('DEBUG', out)

    def test_loglevel_critical_logging_only(self):
        print('Critical logging only')
        self.manager.critical_logging_only = True
        out = self.capture_stderr_call()
        self.assertIn('CRITICAL', out)
        self.assertNotIn('ERROR', out)

    def test_logger_class(self):
        print('Logger class')
        self.assertEqual(str(Logger().logger.__class__),
                         "<class 'logging.RootLogger'>")


if __name__ == '__main__':
    unittest.main()
