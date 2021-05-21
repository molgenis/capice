import os
import unittest
from src.main.python.core.logger import Logger
from src.test.python.test_templates import set_up_manager_and_loc, teardown


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, cls.output_loc = set_up_manager_and_loc()
        cls.manager.log_loc = cls.output_loc
        cls.manager.critical_logging_only = False
        cls.manager.disable_logfile = False
        cls.log = Logger()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def tearDown(self):
        print('Resetting arguments.')
        self.manager.verbose = False
        self.log.create_logfile = False

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
        self.manager.log_loc = self.output_loc
        logger_load = self.log.load_logger()
        handlers = logger_load.parent.handlers
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
        with open(os.path.join(self.output_loc, 'present_file.log'), 'wt') as logfile:
            logfile.write('Already present')
        new_filename = self.log._create_log_export_name(out_file_name='present_file')
        self.assertEqual(os.path.basename(new_filename), 'present_file_1.log')


if __name__ == '__main__':
    unittest.main()
