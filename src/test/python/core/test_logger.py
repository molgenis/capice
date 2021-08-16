import os
import unittest
from datetime import datetime
from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import teardown


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager = CapiceManager()
        cls.output_loc = os.path.join(get_project_root_dir(), '.test_output')
        if not os.path.exists(cls.output_loc):
            os.makedirs(cls.output_loc)
        cls.manager.now = datetime.now()
        cls.manager.log_loc = cls.output_loc
        cls.manager.critical_logging_only = False
        cls.manager.enable_logfile = True
        cls.log = Logger().logger

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')
        self.log = Logger()

    def test_loglevel_nonverbose(self):
        print('Loglevel non verbose')
        loglevel = self.log.set_loglevel()
        self.assertEqual(loglevel, 20)

    def test_loglevel_verbose(self):
        print('Loglevel verbose')
        self.manager.verbose = True
        loglevel = self.log.set_loglevel()
        self.assertEqual(loglevel, 0)

    def test_create_logfile(self):
        print('Creating logfile')
        message = 'This is a test_create_logfile specific ' \
                  'message for testing purposes'
        self.log.logger.info(message)
        expected_out_message = '[CAPICE] ' \
                               '[test_logger.py] ' \
                               '[test_create_logfile] ' \
                               '[INFO]  ' \
                               '{}'.format(message)
        logfile = os.listdir(self.output_loc)[0]
        with open(os.path.join(self.output_loc, logfile), 'rt') as log_messages:
            messages = log_messages.readlines()
        stripped_messages = []
        for log in messages:
            stripped_messages.append(' '.join(log.strip().split(' ')[2:]))
        self.assertIn(expected_out_message, stripped_messages)

    def test_filehandler(self):
        print('Logging filehandler')
        self.manager.log_loc = self.output_loc
        handlers = self.log.logger.handlers
        string_handlers = []
        for handler in handlers:
            string_handlers.append(str(handler.__class__))
        self.assertTrue("<class 'logging.FileHandler'>" in string_handlers)

    def test_final_logloc(self):
        print('Final logloc')
        files_present = []
        for file in os.listdir(self.output_loc):
            files_present.append(os.path.join(self.output_loc, file))
        self.assertTrue(self.log.get_log_loc() in files_present)

    def test_creating_log_filename(self):
        print('Logfile filename')
        with open(
                os.path.join(self.output_loc, 'present_file.log'),
                'wt') as logfile:
            logfile.write('Already present')
        new_filename = self.log._create_log_export_name(
            out_file_name='present_file'
        )
        self.assertEqual(
            new_filename, os.path.join(self.output_loc, 'present_file_1.log')
        )


if __name__ == '__main__':
    unittest.main()
