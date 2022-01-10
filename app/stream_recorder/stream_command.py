from .log_level import LogLevel
from .output_type import OutputType


class StreamCommand(object):
    name: str
    dir: str
    url: str
    options: str
    loglevel: str
    type: OutputType
    extension: str
    duration: int
    interval: int

    # for Videos only
    # duration: int

    # for Images only
    # interval: int
    # quality = 7    [1 - 31, 1 - High, 31 - Lowest]

    def get_command() -> str:
        raise NotImplementedError
