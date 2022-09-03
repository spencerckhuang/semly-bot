from datetime import datetime, timedelta
import pytest
import pytz
from reminder import (
    is_hour_before_hack_session,
    is_check_in_time,
    is_hack_session_time,
)


@pytest.fixture
def timezone():
    return pytz.timezone("America/New_York")


@pytest.fixture
def wednesday(timezone):
    return datetime(2022, 8, 31, 19, 0, 0, tzinfo=timezone)


@pytest.fixture
def sunday(timezone):
    return datetime(2022, 9, 4, 18, 0, 0, tzinfo=timezone)


def test_check_in(sunday: datetime):
    assert is_check_in_time(sunday) is True


def test_not_check_in(sunday: datetime):
    assert is_check_in_time(sunday + timedelta(minutes=1)) is False
    assert is_check_in_time(sunday - timedelta(minutes=1)) is False
    assert is_check_in_time(sunday - timedelta(minutes=30)) is False


def test_before_hack_session(wednesday: datetime):
    assert is_hour_before_hack_session(wednesday - timedelta(minutes=60)) is True


def test_not_before_hack_session(wednesday: datetime):
    assert is_hour_before_hack_session(wednesday + timedelta(minutes=60)) is False
    assert is_hour_before_hack_session(wednesday - timedelta(minutes=61)) is False
    assert is_hour_before_hack_session(wednesday - timedelta(minutes=59)) is False


def test_hack_session(wednesday: datetime):
    assert is_hack_session_time(wednesday) is True


def test_not_hack_session(wednesday: datetime):
    assert is_hack_session_time(wednesday + timedelta(minutes=1)) is False
    assert is_hack_session_time(wednesday - timedelta(minutes=1)) is False
    assert is_hack_session_time(wednesday - timedelta(minutes=60)) is False
