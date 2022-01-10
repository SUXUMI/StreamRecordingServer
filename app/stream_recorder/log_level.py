from enum import Enum


class LogLevel(Enum):
    QUIET = 'quiet'
    PANIC = 'panic'
    FATAL = 'fatal'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'
