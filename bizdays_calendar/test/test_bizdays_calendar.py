"""
Tests for `bizdays_calendar` module.
"""
import pytest
from lib.exceptions import BizdaysException


def test_build_calendar_passing_invalid_calendar_file_should_print_log_message_and_pass():
    raise BizdaysException


def test_build_calendar_not_passing_calendar_file_should_print_log_message_and_pass():
    raise BizdaysException


def test_build_business_days_passing_invalid_calendar_file_should_throw_exception():
    raise BizdaysException


def test_build_business_with_invalid_date_should_throw_exception():
    raise BizdaysException


def test_build_business_days_not_passing_calendar_file_should_throw_exception():
    raise BizdaysException
