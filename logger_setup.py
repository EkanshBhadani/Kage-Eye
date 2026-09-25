# logger_setup.py

import logging
import os


def setup_logger():

    os.makedirs(
        "data",
        exist_ok=True
    )

    logger = logging.getLogger(
        "MALMonitor"
    )

    logger.setLevel(
        logging.INFO
    )

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        "data/monitor.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    return logger
