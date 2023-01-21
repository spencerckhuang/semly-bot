from datetime import datetime, timedelta
import pytest
import pytz
from reminder import (
    is_hour_before_hack_session,
    is_check_in_time,
    is_hack_session_time,
    is_post_hack_session_time,
)


@pytest.fixture
def timezone():
    return pytz.timezone("America/New_York")


@pytest.fixture
def tuesday(timezone):
    return datetime(2023, 1, 24, 20, 0, 0, tzinfo=timezone)


@pytest.fixture
def saturday(timezone):
    return datetime(2023, 1, 21, 18, 0, 0, tzinfo=timezone)


def test_check_in(saturday: datetime):
    assert is_check_in_time(saturday) is True


def test_not_check_in(saturday: datetime):
    assert is_check_in_time(saturday + timedelta(minutes=1)) is False
    assert is_check_in_time(saturday - timedelta(minutes=1)) is False
    assert is_check_in_time(saturday - timedelta(minutes=30)) is False


def test_before_hack_session(tuesday: datetime):
    assert is_hour_before_hack_session(tuesday - timedelta(minutes=60)) is True


def test_not_before_hack_session(tuesday: datetime):
    assert is_hour_before_hack_session(tuesday + timedelta(minutes=60)) is False
    assert is_hour_before_hack_session(tuesday - timedelta(minutes=61)) is False
    assert is_hour_before_hack_session(tuesday - timedelta(minutes=59)) is False


def test_hack_session(tuesday: datetime):
    assert is_hack_session_time(tuesday) is True


def test_not_hack_session(tuesday: datetime):
    assert is_hack_session_time(tuesday + timedelta(minutes=1)) is False
    assert is_hack_session_time(tuesday - timedelta(minutes=1)) is False
    assert is_hack_session_time(tuesday - timedelta(minutes=60)) is False


def test_post_hack_session(tuesday: datetime):
    assert is_post_hack_session_time(tuesday + timedelta(hours=1)) is True


def test_not_post_hack_session(tuesday: datetime):
    assert is_post_hack_session_time(tuesday) is False
    assert is_post_hack_session_time(tuesday + timedelta(minutes=59)) is False
    assert is_post_hack_session_time(tuesday + timedelta(minutes=61)) is False
