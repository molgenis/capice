import logging


def setup_logger(level):
    logging.basicConfig(
        format='%(asctime)s %(levelname)8s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=level)
    logging.captureWarnings(True)
