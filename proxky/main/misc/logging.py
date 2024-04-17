import logging.config

import logging

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


def format_message_cardname(cardname: str, message: str):
    def _truncate_prefix(prefix: str, length: int) -> str:
        truncated_prefix = "["
        truncated_prefix += prefix[:length - 2 - 1 - 3] + "..." if len(prefix) + 2 + 1 > length else prefix
        truncated_prefix += "]"

        for i in range(0, length - len(truncated_prefix)):
            truncated_prefix += " "

        return truncated_prefix

    return f"{_truncate_prefix(cardname, 50)}{message}"


setup()
