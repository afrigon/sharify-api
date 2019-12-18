# -*- coding: utf-8 -*-

from calendar import timegm
from datetime import datetime, timedelta


def now(leeway=0):
    if isinstance(leeway, timedelta):
        leeway = leeway.total_seconds()

    return timegm(datetime.utcnow().utctimetuple()) + leeway
