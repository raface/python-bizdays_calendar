"""
Tests for `bizdays_calendar` module.
"""
import pytest
from context import *
from lib.exceptions import BizdaysException


def test_build_calendar_passing_invalid_calendar_file_should_print_log_message_and_pass():
    Calendar('/home/dev/test.txt')


def test_build_calendar_not_passing_calendar_file_should_print_log_message_and_pass():
    Calendar()


def test_build_calendar_with_output_format_none_should_throw_exception():
    with pytest.raises(BizdaysException):
        Calendar('./test.cal', output_format=None)


def test_build_calendar_with_output_format_invalid_should_throw_exception():
    with pytest.raises(BizdaysException):
        Calendar('./test.cal', output_format='YYYY-MM-DD')


def test_build_calendar_get_holidays_should_return_datetime_list():
    holidays_list = Calendar('./test.cal').get_holidays()
    assert holidays_list == [datetime.datetime(2017, 12, 25, 0, 0), datetime.datetime(2018, 1, 1, 0, 0)]
