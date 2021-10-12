import logging


class Trainer:
    def __init__(self, input_path, impute_path, test_split, output_path):
        self.input_path = input_path
        self.impute_path = impute_path
        self.test_split = test_split
        self.output_path = output_path

    def train(self):
        logging.critical("todo: implement training on '%s' with impute file '%s' and split '%f' to '%s",
                         self.input_path,
                         self.impute_path,
                         self.test_split,
                         self.output_path)
