import unittest

from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent


class TestArgsHandlerPredict(unittest.TestCase):
    CLI_ARGS = '-z/--zz'

    def test__single_argument_retriever_single_none(self):
        test_input = None
        expected_output = None
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     has_default=False)
        self.assertEqual(actual_output, expected_output)

    def test__single_argument_retriever_empty_list(self):
        test_input = []
        with self.assertRaises(ValueError) as context:
            ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                         has_default=False)
        msg = 'Empty list is given. Should be None or list with elements.'
        self.assertEqual(str(context.exception), msg)

    def test__single_argument_retriever_one_item(self):
        test_input = ['aa']
        expected_output = 'aa'
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     has_default=False)
        self.assertEqual(actual_output, expected_output)

    def test__single_argument_retriever_default_only(self):
        test_input = ['aa']
        expected_output = 'aa'
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     has_default=True)
        self.assertEqual(actual_output, expected_output)

    def test__single_argument_retriever_two_items_no_default(self):
        test_input = ['aa', 'bb']
        with self.assertRaises(IOError) as context:
            ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                         has_default=False)
        msg = 'Argument -z/--zz is only allowed once.'
        self.assertEqual(str(context.exception), msg)

    def test__single_argument_retriever_default_with_one_item(self):
        test_input = ['aa', 'bb']
        expected_output = 'bb'
        actual_output = ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                                     has_default=True)
        self.assertEqual(actual_output, expected_output)

    def test__single_argument_retriever_default_with_two_items(self):
        test_input = ['aa', 'bb', 'cc']
        with self.assertRaises(IOError) as context:
            ArgsHandlerParent._single_argument_retriever(test_input, self.CLI_ARGS,
                                                         has_default=True)
        msg = 'Argument -z/--zz is only allowed once.'
        self.assertEqual(str(context.exception), msg)


if __name__ == '__main__':
    unittest.main()


