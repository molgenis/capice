import unittest

from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent


class TestArgsHandlerPredict(unittest.TestCase):
    CLI_ARGS = '-z/--zz'

    def test__retrieve_argument_single_none(self):
        test_input = None
        expected_output = None
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     False)
        self.assertEqual(actual_output, expected_output)

    def test__retrieve_argument_single_empty_list(self):
        test_input = []
        with self.assertRaises(ValueError) as context:
            ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS, False)
        msg = 'Empty list is given. Should be None or list with elements.'
        self.assertEqual(str(context.exception), msg)

    def test__retrieve_argument_single_one_item(self):
        test_input = ['aa']
        expected_output = 'aa'
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     False)
        self.assertEqual(actual_output, expected_output)

    def test__retrieve_argument_single_multi_item_no_default(self):
        test_input = ['aa', 'bb']
        with self.assertRaises(IOError) as context:
            ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS, False)
        msg = 'Argument -z/--zz is only allowed once.'
        self.assertEqual(str(context.exception), msg)

    def test__retrieve_argument_single_multi_item_with_default(self):
        test_input = ['aa', 'bb']
        expected_output = 'bb'
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     True)
        self.assertEqual(actual_output, expected_output)

    def test__retrieve_argument_single_multi_item_no_default(self):
        test_input = ['aa', 'bb', 'cc']
        with self.assertRaises(IOError) as context:
            ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS, True)
        msg = 'Argument -z/--zz is only allowed once.'
        self.assertEqual(str(context.exception), msg)


if __name__ == '__main__':
    unittest.main()


