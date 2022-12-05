import argparse
import unittest

from io import StringIO
from unittest.mock import patch

from molgenis.capice.cli.args_handler_train import ArgsHandlerTrain


class TestArgsHandlerPredict(unittest.TestCase):

    def setUp(self):
        parser = argparse.ArgumentParser(
            description="CAPICE test"
        )
        self.aht = ArgsHandlerTrain(parser)

    @patch('sys.stderr', new_callable=StringIO)
    def test_validate_n_threads(self, stderr):
        with self.assertRaises(SystemExit):
            self.aht.validate_n_threads(0)
        self.assertIn('The amount of threads has to be at least 1!', stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_validate_test_split_0(self, stderr):
        with self.assertRaises(SystemExit):
            self.aht.validate_test_split(0)
        self.assertIn('Test split must be a float between 0 and 1', stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_validate_test_split_1(self, stderr):
        with self.assertRaises(SystemExit):
            self.aht.validate_test_split(1)
        self.assertIn('Test split must be a float between 0 and 1', stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
