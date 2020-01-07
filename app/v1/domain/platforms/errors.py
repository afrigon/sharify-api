from enum import Enum


class PlatformErrorType(Enum):
    THROTTLED = 428
    PARSING = 1000
    AUTH_REFRESH = 1001
