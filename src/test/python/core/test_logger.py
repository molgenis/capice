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

    def setUp(self):
        print('Testing case:')

    def tearDown(self) -> None:
        print('Resetting arguments.')
        Logger.instance = None

    def test_loglevel_nonverbose(self):
        print('Loglevel info')
        log = Logger()
        self.assertEqual(20, log.stdout_loglevels[0])
        self.assertEqual([30, 40, 50], sorted(log.stderr_loglevels))

    def test_loglevel_verbose(self):
        print('Loglevel verbose')
        self.manager.verbose = True
        log = Logger()
        self.assertEqual([10, 20], sorted(log.stdout_loglevels))
        self.manager.verbose = False

    def test_loglevel_critical_logging_only(self):
        print('Critical logging only')
        self.manager.critical_logging_only = True
        log = Logger()
        self.assertEqual(0, len(log.stdout_loglevels))
        self.assertEqual(50, log.stderr_loglevels[0])
        self.manager.critical_logging_only = False

    def test_logger_class(self):
        print('Logger class')
        self.assertEqual(str(Logger().logger.__class__),
                         "<class 'logging.RootLogger'>")

    def test_stdout_call(self):
        print('Logger stdout call')
        old_stdout = sys.stdout
        listener = io.StringIO()
        sys.stdout = listener
        log = Logger().logger
        log.info('SomeString')
        out = listener.getvalue()
        sys.stdout = old_stdout
        interesting_bit = ''.join(out.split('[CAPICE] ')[1:]).strip()
        self.assertEqual(
            '[test_logger.py] [test_stdout_call] [INFO]  SomeString',
            interesting_bit
        )

    def test_stderr_call(self):
        print('Logger stderr call')
        old_stderr = sys.stderr
        listener = io.StringIO()
        sys.stderr = listener
        log = Logger().logger
        log.error('SomeString')
        out = listener.getvalue()
        sys.stderr = old_stderr
        interesting_bit = ''.join(out.split('[CAPICE] ')[1:]).strip()
        self.assertEqual(
            '[test_logger.py] [test_stderr_call] [ERRO]  SomeString',
            interesting_bit
        )


if __name__ == '__main__':
    unittest.main()
