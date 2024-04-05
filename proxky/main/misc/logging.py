import logging
import logging.config

loggers: dict = dict()


def setup():
    global loggers

    logger = logging.getLogger("proxky")
    loggers["proxky"] = logger

    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_format = logging.Formatter("%(asctime)s - [%(name)s] - %(threadName)s - %(levelname)s: %(message)s")
    console_handler.setFormatter(log_format)

    logger.addHandler(console_handler)
    logger.propagate = False


def get_logger(logger_designation: str = "proxky") -> logging.Logger:
    if logger_designation is None:
        logger_designation = "proxky"

    if logger_designation not in loggers:
        loggers[logger_designation] = logging.getLogger(logger_designation)

    return loggers[logger_designation]


setup()
