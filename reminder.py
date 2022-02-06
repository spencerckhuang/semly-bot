from datetime import datetime


def is_30_minutes_before_check_in(time: datetime) -> bool:
    return time.weekday() == 0 and time.hour == 10 and time.minute == 30


def is_check_in_time(time: datetime) -> bool:
    return time.weekday() == 0 and time.hour == 11 and time.minute == 0


def is_30_minutes_before_hack_session(time: datetime) -> bool:
    return time.weekday() == 3 and time.hour == 15 and time.minute == 30


def is_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 3 and time.hour == 16 and time.minute == 0
