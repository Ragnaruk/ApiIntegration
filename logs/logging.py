import logging
import sys

from config.config import path_logs_directory


def get_logger(logger_name, logging_level):
    """
    Get a logger object that writes to logs directory and to stdout.

    :param logger_name: Name of the logger and the log file
    :param logging_level: Level of log messages (ERROR, INFO, DEBUG)
    :return: Logger object
    """
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging_level)

    logger_handler = logging.FileHandler(path_logs_directory / (logger_name + '.log'))
    logger_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )

    logger.addHandler(logger_handler)

    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )

    logger.addHandler(logger_handler)

    return logger
