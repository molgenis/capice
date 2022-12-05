import unittest
from argparse import ArgumentParser

from molgenis.capice.cli.args_handler_explain import ArgsHandlerExplain


class TestArgsHandlerExplain(unittest.TestCase):
    def test_property_str_versions(self):
        args_handler = ArgsHandlerExplain(ArgumentParser())
        self.assertEqual('.json, .ubj', args_handler._extension_str())
        self.assertEqual('.tsv, .tsv.gz', args_handler._required_output_extensions_str())


if __name__ == '__main__':
    unittest.main()
