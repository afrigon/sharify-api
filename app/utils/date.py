from calendar import timegm
from datetime import datetime, timedelta, date


def now(leeway=0):
    if isinstance(leeway, timedelta):
        leeway = leeway.total_seconds()

    return timegm(datetime.utcnow().utctimetuple()) + leeway


def today():
    return str(date.today())
