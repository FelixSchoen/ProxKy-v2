import enum

from proxky.configuration.variables import Colors


class InfoMode(enum.Enum):
    NORMAL = Colors.END
    SUCCESS = Colors.GREEN
    WARN = Colors.ORANGE
    ERROR = Colors.RED


class ProcessMode(enum.Enum):
    ADVENTURE = "adventure"
    REVERSIBLE = "reversible"
