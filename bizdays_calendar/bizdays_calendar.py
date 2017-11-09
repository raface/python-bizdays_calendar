from utils.exceptions import FormattingException, FileException, BizdaysException
from utils.logging import LoggingMixin
import datetime
from dateutil.relativedelta import relativedelta
import csv
import re
import os


class Calendar(LoggingMixin):
    """
    Calendar class will create an object with a list of holidays and
        it will allow to do some date validation.
    :param holidays_file: The file path for holidays calendar file. The calendar file
        must contain strings with the following format YYYYMMDD or YYMMDD and using
        the following separators: - or / or . or _
    :type holidays_file: string
    :param output_format: The string output format for dates. It must follow
        strftime() and strptime() behavior.
    :type output_format: string
    """

    def __init__(self, holidays_file=None, output_format='%Y/%m/%d'):
        self.holidays_file = holidays_file
        self.holidays = []
        self.date_output_format_validation(output_format)
        self.output_format = output_format
        self.open_file()

    def open_file(self):
        """
        Functions that reads holidays_file and append each line, if valid, to attribute holidays
        """
        try:
            with open(self.holidays_file, mode="r") as infile:
                reader = csv.reader(infile)
                for line in reader:
                    self.holidays.append(self.string_to_datetime(line[0]))
        except:
            self.log.debug('Calendar file {} is not valid. Holidays will not be defined.'.format(self.holidays_file))

    def date_input_format_validation(self, date_string):
        """
        Functions that validates if a date string is following the formats YYYYMMDD or YYMMDD
        and using the following separators: - or / or . or _
        :param date_string: A string representation of a date
        :type date_string: string
        """
        date_string_validate = re.compile('^(\d{2,4})([-/:._|])(0[1-9]|1[0-2])([-/:._|])(3[01]|[12][0-9]|0[1-9])$')
        if not date_string:
            raise FormattingException("Output format cannot be None.")
        if not date_string_validate.match(date_string):
            raise FormattingException("\"{}\" is not a valid date format. Please choose between: \"%Y/%m/%d\","
                                      " \"%Y-%m-%d\" or check strftime and strptime behavior.".format(date_string))

    def string_to_datetime(self, sourcedate):
        """
        Functions that converts string to datetime object
        :param sourcedate: A string representation of date
        :type sourcedate: string
        :return: datetime object
        """
        self.date_input_format_validation(sourcedate)
        filtered_date = re.sub(r"^(\d{2,4})([-/:._|])(0[1-9]|1[0-2])([-/:._|])(3[01]|[12][0-9]|0[1-9])$", r"\1\3\5",
                               sourcedate)
        for fmt in ('%y%m%d', '%Y%m%d'):
            try:
                return datetime.datetime.strptime(filtered_date, fmt)
            except ValueError:
                self.log.debug(
                    'The date {0} does not have a valid date format {1}. Returned none.'.format(filtered_date, fmt))

    @staticmethod
    def datetime_to_string(sourcedate, output_format="%Y/%m/%d"):
        """
        Functions that converts datetime object to string
        :param sourcedate: A string representation of date
        :type sourcedate: string
        :param output_format: The string output format for dates. It must follow strftime() and strptime() behavior.
        :type output_format: string
        :return: string
        """
        return sourcedate.strftime(output_format)

    @staticmethod
    def date_output_format_validation(date_string):
        """
        Functions that validates if string output format for dates follows
        strftime() and strptime() behavior.
        :param date_string: A string representation of a date
        :type date_string: string
        """
        date_string_validate = re.compile('(.*)(%-?[\w])(.)(%-?[\w])(.)(%-?[\w])(.*)')
        if not date_string:
            raise FormattingException("Output format cannot be None.")
        if not date_string_validate.match(date_string):
            raise FormattingException("\"{}\" is not a valid date format. Please choose between: \"%Y/%m/%d\", "
                                      "\"%Y-%m-%d\" or check strftime and strptime behavior.".format(date_string))

    def get_holidays(self):
        """
        Function to return holidays attributes
        :return: Array list of holidays.
        """
        return self.holidays


class Businessdays(Calendar):
    """
    Businessdays is derived from Calendar class.
    Businessdays class will create an object with a list of holidays, allow to do some date calculation
    and check if the result is a business day or not.
    :param holidays_file: The file path for holidays calendar file. The calendar file
        must contain strings with the following format YYYYMMDD or YYMMDD and using
        the following separators: - or / or . or _
    :type holidays_file: string
    :param output_format: The string output format for dates. It must follow
        strftime() and strptime() behavior.
    :type output_format: string
    :param sourcedate: A string representation of a date with the following
    format YYYYMMDD or YYMMDD and using the following separators: - or / or . or _
    :type sourcedate: string
    """

    def __init__(self, sourcedate, holidays_file, output_format='%Y/%m/%d'):
        self.date_input_format_validation(sourcedate)
        self.date_output_format_validation(output_format)
        self.output_format = output_format
        self.sourcedate = sourcedate
        if not isinstance(self.sourcedate, datetime.datetime):
            self.sourcedate = self.string_to_datetime(sourcedate)
        if not holidays_file or not os.path.isfile(holidays_file) or os.stat(holidays_file).st_size == 0:
            raise FileException("Holiday file {} is empty. Existing because Businessdays need it."
                                .format(holidays_file))
        self.holidays_file = holidays_file
        super(Businessdays, self).__init__(self.holidays_file, self.output_format)

    def date_calculator(self, years=0, months=0, days=0):
        """
        Functions to do arithmetic operations with the parsed date.
        :param years: An arithmetic operator and an integer value
        :type years: int
        :param months: An arithmetic operator and an integer value
        :type months: int
        :param days: An arithmetic operator and an integer value
        :type days: int
        :return: sourcedate attribute after arithmetic operations
        """
        try:
            self.sourcedate = self.sourcedate + relativedelta(years=years)
            self.sourcedate = self.sourcedate + relativedelta(months=months)
            self.sourcedate = self.sourcedate + relativedelta(days=days)
        except (ValueError, TypeError) as e_info:
            raise FormattingException('The date calculation for {0} failed: {1}. Returned none.'.format(self.sourcedate, e_info))
        return self

    def get_date(self):
        """
        Functions that returns sourcedate attribute as string
        :return: sourcedate attribute as string
        """
        if isinstance(self.sourcedate, datetime.datetime):
            self.sourcedate = self.datetime_to_string(self.sourcedate, output_format=self.output_format)
        return self.sourcedate

    def is_business_day(self):
        """
        Functions that verify if sourcedate attribute is a business day.
        """
        if self.sourcedate.isoweekday() in {6, 7} or self.sourcedate in self.holidays:
            return False
        else:
            return True

    def next_business_day(self):
        """
        Functions that return the next business day of sourcedate attribute.
        :return: sourcedate attribute as string
        """
        return self.__move_business_day__(1)

    def prev_business_day(self):
        """
        Functions that return the previous business day of sourcedate attribute.
        :return: sourcedate attribute as string
        """
        return self.__move_business_day__(-1)

    def get_business_day(self, timedelta=0):
        """
        Functions that return sourcedate attribute after arithmetic operations using timedelta argument.
        :param timedelta: An arithmetic operator and an integer value
        :type timedelta: int
        :return: sourcedate attribute as string
        """
        return self.__move_business_day__(timedelta)

    def __move_business_day__(self, days_to_move):
        """
        Functions that return sourcedate attribute after arithmetic operations using days_to_move argument.
        :param days_to_move: An arithmetic operator and an integer value
        :type days_to_move: int
        :return: sourcedate attribute as string
        """
        if days_to_move is None:
            raise BizdaysException("days_to_move argument cannot be None.")
        self.sourcedate = self.sourcedate + relativedelta(days=days_to_move)
        if not self.is_business_day() and days_to_move == 0:
            raise BizdaysException("days_to_move argument cannot be 0 if sourcedate is a non business day.")
        while not self.is_business_day():
            self.sourcedate = self.sourcedate + relativedelta(days=days_to_move)
        return self

    def format_date(self, output_string):
        """
        Takes an output string and outputs that string
        with the source date with the specified time format
        :param output_string: output string format  E.g. %Y-%m-%d
        :type output_string: str
        :return: S

        >>> Businessdays('2017/09/25', './test/test.cal').format_date("~/dev/code.%y.%m.%d")
        '~/dev/code.17.09.25'
        >>> Businessdays('2017/06/30', './test/test.cal').format_date("~/dev/code/file%Y%m%d")
        '~/dev/code/file20170630'
        """
        self.date_output_format_validation(output_string)
        return self.sourcedate.strftime(output_string)
