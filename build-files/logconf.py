import logging


def get_logger():
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s:%(levelname)s:  %(message)s")
    logger = logging.getLogger(__name__)
    return logger

