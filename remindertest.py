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
def wednesday(timezone):
    return datetime(2022, 2, 23, 11, 0, 0, tzinfo=timezone)


@pytest.fixture
def saturday(timezone):
    return datetime(2022, 2, 26, 14, 0, 0, tzinfo=timezone)


def test_before_check_in(wednesday: datetime):
    assert is_half_hour_before_check_in(wednesday - timedelta(minutes=30)) is True


def test_not_before_check_in(wednesday: datetime):
    assert is_half_hour_before_check_in(wednesday + timedelta(minutes=30)) is False
    assert is_half_hour_before_check_in(wednesday - timedelta(minutes=31)) is False
    assert is_half_hour_before_check_in(wednesday - timedelta(minutes=29)) is False


def test_check_in(wednesday: datetime):
    assert is_check_in_time(wednesday) is True


def test_not_check_in(wednesday: datetime):
    assert is_check_in_time(wednesday + timedelta(minutes=1)) is False
    assert is_check_in_time(wednesday - timedelta(minutes=1)) is False
    assert is_check_in_time(wednesday - timedelta(minutes=30)) is False


def test_before_hack_session(saturday: datetime):
    assert is_hour_before_hack_session(saturday - timedelta(minutes=60)) is True


def test_not_before_hack_session(saturday: datetime):
    assert is_hour_before_hack_session(saturday + timedelta(minutes=60)) is False
    assert is_hour_before_hack_session(saturday - timedelta(minutes=61)) is False
    assert is_hour_before_hack_session(saturday - timedelta(minutes=59)) is False


def test_hack_session(saturday: datetime):
    assert is_hack_session_time(saturday) is True


def test_not_hack_session(saturday: datetime):
    assert is_hack_session_time(saturday + timedelta(minutes=1)) is False
    assert is_hack_session_time(saturday - timedelta(minutes=1)) is False
    assert is_hack_session_time(saturday - timedelta(minutes=60)) is False
