import logging


class Predicter:
    def __init__(self, input_path, model_path, output_path):
        self.input_path = input_path
        self.model_path = model_path
        self.output_path = output_path

    def predict(self):
        logging.critical("todo: implement prediction on '%s' with '%s' to '%s",
                         self.input_path,
                         self.model_path,
                         self.output_path)
