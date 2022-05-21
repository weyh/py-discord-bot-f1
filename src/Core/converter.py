# -*- coding: utf-8 -*
from whenareyou import whenareyou
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone


def str2bool(string: str) -> bool:
    'Converts str to bool'
    return string.lower() in ("true", "t")


def to_local_time(loc: str, loc_dt: datetime) -> datetime | None:
    tz = whenareyou(loc)
    if tz is None:
        return None

    tzone = timezone(tz)
    return tzone.localize(loc_dt).astimezone(get_localzone())
