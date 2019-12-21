# -*- coding: utf-8 -*-

from enum import Enum


class ErrorType(Enum):
    THROTTLED = 428
    PARSING = 1000
    AUTH_REFRESH = 1001
