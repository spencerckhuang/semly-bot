from datetime import datetime, timedelta
import pytest
import pytz
from reminder import (
    is_half_hour_before_check_in,
    is_hour_before_hack_session,
    is_check_in_time,
    is_hack_session_time,
)


@pytest.fixture
def timezone():
    return pytz.timezone("America/New_York")


@pytest.fixture
def monday(timezone):
    return datetime(2022, 2, 7, 11, 0, 0, tzinfo=timezone)


@pytest.fixture
def thursday(timezone):
    return datetime(2022, 2, 10, 16, 0, 0, tzinfo=timezone)


def test_before_check_in(monday: datetime):
    assert is_half_hour_before_check_in(monday - timedelta(minutes=30)) is True


def test_not_before_check_in(monday: datetime):
    assert is_half_hour_before_check_in(monday + timedelta(minutes=30)) is False
    assert is_half_hour_before_check_in(monday - timedelta(minutes=31)) is False
    assert is_half_hour_before_check_in(monday - timedelta(minutes=29)) is False


def test_check_in(monday: datetime):
    assert is_check_in_time(monday) is True


def test_not_check_in(monday: datetime):
    assert is_check_in_time(monday + timedelta(minutes=1)) is False
    assert is_check_in_time(monday - timedelta(minutes=1)) is False
    assert is_check_in_time(monday - timedelta(minutes=30)) is False


def test_before_hack_session(thursday: datetime):
    assert is_hour_before_hack_session(thursday - timedelta(minutes=60)) is True


def test_not_before_hack_session(thursday: datetime):
    assert is_hour_before_hack_session(thursday + timedelta(minutes=60)) is False
    assert is_hour_before_hack_session(thursday - timedelta(minutes=61)) is False
    assert is_hour_before_hack_session(thursday - timedelta(minutes=59)) is False


def test_hack_session(thursday: datetime):
    assert is_hack_session_time(thursday) is True


def test_not_hack_session(thursday: datetime):
    assert is_hack_session_time(thursday + timedelta(minutes=1)) is False
    assert is_hack_session_time(thursday - timedelta(minutes=1)) is False
    assert is_hack_session_time(thursday - timedelta(minutes=60)) is False
