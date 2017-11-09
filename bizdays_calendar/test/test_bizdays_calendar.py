"""
Tests for `bizdays_calendar` module.
"""
import pytest
from context import *
from utils.exceptions import FormattingException, FileException, BizdaysException


def calculate_date(business_days, years=0, months=0, days=0):
    return business_days.date_calculator(years, months, days)


def build_business_days(date, output_format="%Y/%m/%d", holidays_file='./test.cal'):
    return Businessdays(date, holidays_file=holidays_file, output_format=output_format)


def test_build_calendar_passing_invalid_calendar_file_should_print_log_message_and_instanciate_calendar_class():
    cal = Calendar('/home/dev/test.txt')
    assert isinstance(cal, Calendar)


def test_build_calendar_not_passing_calendar_file_should_print_log_message_and_instanciate_calendar_class():
    cal = Calendar()
    assert isinstance(cal, Calendar)


def test_build_calendar_with_output_format_none_should_throw_exception():
    with pytest.raises(FormattingException):
        Calendar('./test.cal', output_format=None)


def test_build_calendar_with_output_format_invalid_should_throw_exception():
    with pytest.raises(FormattingException):
        Calendar('./test.cal', output_format='YYYY-MM-DD')


def test_build_calendar_passing_none_date_string_should_throw_exception():
    with pytest.raises(FormattingException):
        new_date_string = Calendar('./test.cal').date_input_format_validation(date_string=None)


def test_build_calendar_get_holidays_should_return_datetime_list():
    holidays_list = Calendar('./test.cal').get_holidays()
    assert holidays_list == [datetime.datetime(2017, 12, 25, 0, 0), datetime.datetime(2018, 1, 1, 0, 0)]


def test_build_business_days_passing_invalid_calendar_file_should_throw_exception():
    with pytest.raises(FileException):
        business_days = build_business_days('2017/08/09', holidays_file='/home/dev/test.txt')


def test_build_business_days_passing_empty_calendar_file_should_throw_exception():
    with pytest.raises(FileException):
        business_days = build_business_days('2017/08/09', holidays_file='./test/empty.cal')


def test_build_business_days_not_passing_calendar_file_should_throw_exception():
    with pytest.raises(FileException):
        business_days = build_business_days('2017/08/09', holidays_file=None)


def test_build_business_with_invalid_date_should_throw_exception():
    with pytest.raises(FormattingException):
        business_days = build_business_days('99999/999/999')

def test_business_days_passing_output_format_should_return_string_following_passed_output_format():
    business_days = build_business_days('2018.01.02', output_format="%y-%m-%d").get_date()
    assert business_days == "18-01-02"


def test_can_add_one_year():
    business_days = build_business_days('2000/02/29')
    calculated_date = calculate_date(business_days, years=1)
    assert calculated_date.get_date() == '2001/02/28'


def test_can_add_one_month():
    business_days = build_business_days('2000/02/29')
    calculated_date = calculate_date(business_days, months=1)
    assert calculated_date.get_date() == '2000/03/29'


def test_can_add_one_day():
    business_days = build_business_days('2000/02/29')
    calculated_date = calculate_date(business_days, days=1)
    assert calculated_date.get_date() == '2000/03/01'


def test_calculated_date_passing_none_should_print_log_message():
    with pytest.raises(FormattingException):
        business_days = build_business_days('2000/02/29')
        calculated_date = calculate_date(business_days, days=None)


def test_get_next_business_day_adding_one_year_one_month_one_day():
    business_days = build_business_days('2000/02/29')
    calculated_date = calculate_date(business_days, years=1, months=1, days=1)
    assert calculated_date.next_business_day().get_date() == '2001/03/30'


def test_get_previous_business_day_adding_one_year_one_month_one_day():
    business_days = build_business_days('2000.02.29')
    calculated_date = calculate_date(business_days, years=1, months=1, days=1)
    assert calculated_date.prev_business_day().get_date() == '2001/03/28'


def test_get_next_business_day():
    business_days = build_business_days('2017_12_29')
    assert business_days.next_business_day().get_date() == '2018/01/02'


def test_get_previous_business_day():
    business_days = build_business_days('2018.01.02')
    assert business_days.prev_business_day().get_date() == '2017/12/29'


def test_get_previous_business_day_and_format_date_method_should_return_formated_string():
    business_days = build_business_days('2018.01.02')
    assert business_days.prev_business_day().format_date("/bns/mrm/intray/daily/market.%y.%m.%d") == '/bns/mrm/intray/daily/market.17.12.29'

def test_get_business_day_with_timedelta_0_and_date_is_non_business_day_should_throw_exception():
    with pytest.raises(BizdaysException):
        business_days = build_business_days('2018/01/01')
        assert business_days.get_business_day(timedelta=0)

def test_get_business_day_with_timedelta_none_should_throw_exception():
    with pytest.raises(BizdaysException):
        business_days = build_business_days('2018.01.02')
        assert business_days.get_business_day(timedelta=None)


def test_is_business_day_with_business_day_should_be_true():
    business_days = build_business_days('18.01.02')
    assert business_days.is_business_day()


def test_is_business_day_with_non_business_day_should_be_false():
    business_days = build_business_days('18|01|01')
    assert not business_days.is_business_day()


def test_format_date_with_invalid_format_should_raise_exception():
    with pytest.raises(FormattingException):
        business_days = build_business_days('2017/09/25')
        output_string = business_days.format_date("/bns/mrm/intray/daily/market.YYYY.MM.DD")


def test_format_date_should_output_string_with_passed_date():
    business_days = build_business_days('2017/09/25')
    output_string = business_days.format_date("/bns/mrm/intray/daily/market.%y.%m.%d")
    assert output_string == '/bns/mrm/intray/daily/market.17.09.25'
