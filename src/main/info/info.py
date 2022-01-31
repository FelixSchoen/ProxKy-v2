from enum import Enum

from src.main.configuration.variables import Colors


class INFO_MODE(Enum):
    normal = Colors.END
    success = Colors.GREEN
    warn = Colors.ORANGE
    error = Colors.RED


def show_info(message: str, prefix: str = "ProxKy", mode: INFO_MODE = INFO_MODE.normal, normalize_length=50,
              end_line=True) -> None:
    """
    Prints info message to terminal.
    :param message: Message to print
    :param prefix: Prefix to prepend to the message
    :param mode: How to format the message
    :param normalize_length: Message prefix will be fixed to this size
    """
    print(f"{mode.value}{_truncate_prefix(prefix, normalize_length)}{Colors.END}{message}",
          end="\n" if end_line else "")


def _truncate_prefix(prefix: str, length: int) -> str:
    truncated_prefix = "["
    truncated_prefix += prefix[:length - 2 - 3] + "..." if len(prefix) - 2 > length else prefix
    truncated_prefix += "]"

    for i in range(0, length - len(truncated_prefix)):
        truncated_prefix += " "

    return truncated_prefix
