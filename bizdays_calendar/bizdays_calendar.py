from lib.exceptions import BizdaysException
from lib.logging import LoggingMixin
import datetime
import csv
import re


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
            raise BizdaysException("Output format cannot be None.")
        if not date_string_validate.match(date_string):
            raise BizdaysException("\"{}\" is not a valid date format. Please choose between: \"%Y/%m/%d\", "
                               "\"%Y-%m-%d\" or check strftime and strptime behavior.".format(date_string))

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
            raise BizdaysException("Output format cannot be None.")
        if not date_string_validate.match(date_string):
            raise BizdaysException("\"{}\" is not a valid date format. Please choose between: \"%Y/%m/%d\", "
                               "\"%Y-%m-%d\" or check strftime and strptime behavior.".format(date_string))

    def get_holidays(self):
        """
        Function to return holidays attributes
        :return: Array list of holidays.
        """
        return self.holidays
