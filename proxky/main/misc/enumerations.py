import enum

from proxky.main.configuration.variables import Colors


class InfoMode(enum.Enum):
    NORMAL = Colors.END
    SUCCESS = Colors.GREEN
    WARN = Colors.ORANGE
    ERROR = Colors.RED