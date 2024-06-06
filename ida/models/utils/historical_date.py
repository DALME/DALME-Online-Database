"""Custom class for handling historical dates."""

import calendar
import datetime
import json
import math

import pandas as pd
from dateutil import parser

from django.utils.functional import cached_property


class HistoricalDateRange(dict):
    """Class for managing date ranges throughout the app, even if ambiguous or incomplete.

    Like, HistoricalDate, the class subclasses 'dict' to make the object directly serializable
    by the default encoder.

    HistoricalDateRange takes two arguments, a 'start_date' and an 'end_date', both of which have
    to be instances of 'HistoricalDate'.

    The 'format' method takes up to three arguments:
        - separator: a string used to separate start and end dates, e.g. '-' or ' to '
        - start_date_format: a string with codes following the 1989C standard (same as strftime),
            if no other argument is provided, the same string is used to format the end date
        - end_date_format: same as above for the end date.
    """

    def __new__(cls, start_date, end_date):
        """Return a HistoricalDate instance if both dates are identical."""
        if isinstance(start_date, HistoricalDate) and isinstance(end_date, HistoricalDate) and start_date == end_date:
            return start_date
        return super().__new__(cls, start_date, end_date)

    def __init__(self, start_date, end_date):
        if not start_date or not end_date:
            message = 'Both a start date and an end date must be supplied.'
            raise ValueError(message)

        for date in [start_date, end_date]:
            if not isinstance(date, HistoricalDate):
                message = "The dates supplied must be instances of 'HistoricalDate'."
                raise TypeError(message)

        if start_date == end_date:
            self.value = start_date

        if start_date > end_date:
            self.start = end_date
            self.end = start_date
        else:
            self.start = start_date
            self.end = end_date

        self.text = self.get_range_string()
        self.is_range = True
        self.is_valid = self.start.is_valid and self.end.is_valid
        dict.__init__(self, **self.serialize())

    def __str__(self):
        return self.get_range_string()

    def __dict__(self):
        return self.serialize()

    def __hash__(self):
        return hash(
            self.start.is_bce,
            self.start.day,
            self.start.month,
            self.start.year,
            self.start.text,
            self.end.is_bce,
            self.end.day,
            self.end.month,
            self.end.year,
            self.end.text,
        )

    def __eq__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(other, HistoricalDate):
            return False
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(other, HistoricalDate):
            return self.start.get_as_months() < other.get_as_months()
        return self.start.get_as_months() < other.start.get_as_months()

    def __le__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        return self.__lt__(other) or self.__eq__(other)

    def __ne__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(other, HistoricalDate):
            return self.end.get_as_months() < other.get_as_months()
        return self.end.get_as_months() < other.end.get_as_months()

    def __ge__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        return self.__gt__(other) or self.__eq__(other)

    def __contains__(self, item):
        if not isinstance(item, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(item, HistoricalDateRange):
            return item.start >= self.start and item.end <= self.end
        return self.start <= item <= self.end

    @cached_property
    def is_bce(self):
        """Return boolean indicating whether the range is outside the CE."""
        return self.start.is_bce and self.end.is_bce

    @property
    def day(self):
        """Return a string with a range of days (mostly for compatibility with HistoricalDate)."""
        return [self.start.day, self.end.day]

    @property
    def month(self):
        """Return a string with a range of months (mostly for compatibility with HistoricalDate)."""
        return [self.start.month, self.end.month]

    @property
    def year(self):
        """Return a range of years if both dates have them, otherwise a string."""
        return [
            self.start.get_era(add_year=True) if self.start.is_bce else self.start.year,
            self.end.get_era(add_year=True) if self.end.is_bce else self.end.year,
        ]

    @cached_property
    def date(self):
        """Return a pandas date_range object if both dates are complete."""
        if self.start.date and self.end.date:
            return pd.date_range(start=self.start.date, end=self.end.date)
        return None

    def serialize(self):
        """Return a JSON-serialized version of the date range."""
        return {
            'is_range': True,
            'start': self.start.serialize(),
            'end': self.end.serialize(),
            'text': self.text,
        }

    def get_range_string(self):
        """Return date range as a string."""
        days = [i if i else '?' for i in self.day]
        months = list(set(self.month))
        years = list(set(self.year))
        if len(years) == 1:
            if len(months) == 1:
                return f'{days[0]} to {days[1]}-{calendar.month_abbr[months[0]]}-{years[0]}'
            return (
                f'{days[0]}-{calendar.month_abbr[months[0]]} to {days[1]}-{calendar.month_abbr[months[1]]}-{years[0]}'
            )
        return f'{self.start} to {self.end}'

    def format(self, separator, start_date_format, end_date_format=None):
        """Return the date range as a formatted string."""
        for arg in [separator, start_date_format]:
            if not arg or not isinstance(arg, str):
                message = (
                    'The "format" method takes a string with a separator, a second format string with codes'
                    ' following the 1989C standard (strftime), and an optional third format string. If both format'
                    ' strings are provided, the first one is used for the start date and the second for the end date.'
                )
                raise ValueError(message)

        if not end_date_format:
            end_date_format = start_date_format

        return f'{self.start.format(start_date_format)}{separator}{self.end.format(end_date_format)}'


class HistoricalDate(dict):
    """Class for managing dates throughout the app, even if ambiguous or incomplete.

    We subclass 'dict' to make the object directly serializable by the default encoder.

    The class takes data as argument in one of the following formats:
        - Python datetime.datetime or datetime.date object
        - A list or tuple with three numeric values (int | str) in the form: (year, month, day)
        - A Python dictionary with any or all of the following keys:
            - 'year': 1-4 digit number (int | str)
            - 'month': 1-2 digit positive number as int | str
            - 'day': 1-2 digit positive number as int | str
            - 'date': datetime object or parseable string
            - 'text': str
        - A string:
            - either parseable by the 'dateutil' date parser
            - or containing a JSON representation of the aforementioned dictionary

    Additionally, the keyword argument 'is_bce' can be used to indicate if the date should be
    considered as such. If an object is passed (dict or JSON string), the key 'era' can be used
    to specify the same information:
            - 'era': a string, e.g. BC, BCE, AD, CE, B.C., A.D.

    The 'format' method takes a string with codes following the 1989C standard (same as strftime),
    with these additional format codes:
        - %E: to include era using BCE/CE
        - %EL: to include era using BC/AD system
        - %Ey: to include the year with era using BCE/CE system
        - %ELy: to include the year with era using BC/AD system
    """

    def __init__(self, data, is_bce=False):  # noqa: C901, PLR0912
        if not data:
            message = 'A date in a valid format must be supplied.'
            raise ValueError(message)

        if not isinstance(is_bce, bool):
            message = 'The "is_bce" argument must be a boolean.'
            raise TypeError(message)

        self.is_range = False  # for compatibility with HistoricalDateRange
        self.is_uncertain = False
        self.is_bce = is_bce
        self.day = None
        self.month = None
        self.year = None
        self.date = None
        self.text = None
        self.is_valid = False

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                try:
                    data = parser.parse(data)
                except parser.ParserError as e:
                    message = 'The data supplied could not be parsed into a valid date.'
                    raise ValueError(message) from e

        if isinstance(data, (datetime.date | datetime.datetime)):
            self.day = data.day
            self.month = data.month
            self.year = data.year
            self.date = datetime.date(self.year, self.month, self.day)

        elif isinstance(data, (list | tuple)):
            if len(data) != 3:  # noqa: PLR2004
                message = 'If passing a list/tuple as data, it must contain three values: year, month, day.'
                raise ValueError(message)

            self.year = self.get_as_int(data[0], 'year')
            self.month = self.get_as_int(data[1], 'month')
            self.day = self.get_as_int(data[2], 'day')

        elif isinstance(data, dict):
            self.day, self.month, self.year, self.date, self.text = self.dict_to_date(data)

        if self.day and self.month and self.year and not self.date:
            try:
                self.date = datetime.date(self.year, self.month, self.day)
            except ValueError:
                self.date = parser.parse(f'{self.year!s}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}')

        if not self.text:
            self.text = self.get_date_string()

        self.is_valid = self.validate()
        dict.__init__(self, **self.serialize())

    def __str__(self):
        return self.get_date_string()

    def __dict__(self):
        return self.serialize()

    def __hash__(self):
        return hash(self.is_bce, self.day, self.month, self.year, self.text)

    def __eq__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(other, HistoricalDateRange):
            return False
        if (self.date and other.date) and not (self.is_bce or other.is_bce):
            return self.date == other.date
        return (
            self.day == other.day
            and self.month == other.month
            and self.year == other.year
            and self.is_bce == other.is_bce
        )

    def __lt__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(other, HistoricalDateRange):
            return self.get_as_months() < other.start.get_as_months()
        if (self.date and other.date) and not (self.is_bce or other.is_bce):
            return self.date < other.date
        return self.get_as_months() < other.get_as_months()

    def __le__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        return self.__lt__(other) or self.__eq__(other)

    def __ne__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        if isinstance(other, HistoricalDateRange):
            return self.get_as_months() < other.end.get_as_months()
        if (self.date and other.date) and not (self.is_bce or other.is_bce):
            return self.date > other.date
        return self.get_as_months() > other.get_as_months()

    def __ge__(self, other):
        if not isinstance(other, (HistoricalDate | HistoricalDateRange)):
            return NotImplemented
        return self.__gt__(other) or self.__eq__(other)

    def dict_to_date(self, data):
        day = self.get_as_int(data['day'], 'day') if data.get('day') else None
        month = self.get_as_int(data['month'], 'month') if data.get('month') else None
        year = self.get_as_int(data['year'], 'year') if data.get('year') else None
        text = data.get('text')

        if data.get('era'):
            era = ''.join([i for i in data['era'].lower() if i in 'abcde'])
            self.is_bce = 'bc' in era

        date = data.get('date')
        if isinstance(date, (datetime.date | datetime.datetime)):
            date = datetime.date(date.year, date.month, date.day)
        elif isinstance(date, str):
            try:
                date_obj = parser.parse(date)
                date = datetime.date(date_obj.year, date_obj.month, date_obj.day)
            except parser.ParserError as e:
                date = None
                if not all(self.day, self.month, self.year):
                    message = 'The "date" value could not be parsed into a valid date.'
                    raise ValueError(message) from e

        return (day, month, year, date, text)

    def get_era(self, use_ad=False, add_year=False):
        if add_year:
            if not self.year:
                return None

            templates = {  # order: is_bce, use_ad
                (True, True): '{} BC',
                (True, False): '{} BCE',
                (False, True): 'AD {}',
                (False, False): '{} CE',
            }
            return templates.get((self.is_bce, use_ad)).format(self.year)

        if self.is_bce:
            return 'BC' if use_ad else 'BCE'
        return 'AD' if use_ad else 'CE'

    def get_date_string(self):
        """Return date string."""
        if self.date is not None:
            string = self.date.strftime('%d-%b-%Y').lstrip('0').replace(' 0', ' ')
            return f'{string} BCE' if self.is_bce else string

        if self.month is not None and self.year is not None:
            string = f'{calendar.month_abbr[self.month]}/{self.year}'
            return f'{string} BCE' if self.is_bce else string

        if self.day is not None and self.month is not None:
            return f'{self.day}/{calendar.month_abbr[self.month]}'

        if self.year is not None:
            return f'{self.year} BCE' if self.is_bce else str(self.year)

        if self.text:
            return self.text

        return 'Unknown date'

    def serialize(self):
        """Return a JSON-serialized version of the date."""
        return {
            'is_range': False,
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'date': self.date.isoformat() if isinstance(self.date, datetime.date) else None,
            'text': self.text,
            'era': self.get_era(),
        }

    def validate(self):
        if not any([self.day, self.month, self.year, self.date, self.text]):
            message = 'The data contains no valid date.'
            raise ValueError(message)

        if self.day and not 1 <= self.day <= 31:  # noqa: PLR2004
            message = 'The value for day must be between 1 and 31.'
            raise ValueError(message)

        if self.month and not 1 <= self.month <= 12:  # noqa: PLR2004
            message = 'The value for month must be between 1 and 12.'
            raise ValueError(message)

        return True

    @staticmethod
    def get_as_int(val, prop):
        try:
            return int(abs(val))
        except Exception() as e:
            message = f'The value for "{prop}" must be numeric (int or str).'
            raise ValueError(message) from e

    def get_as_months(self):
        """Return month/year as a count of months."""
        value = 0
        if self.year:
            value += 12 * self.year
        if self.month:
            value += self.month
        if self.is_bce:
            value *= -1
        return value

    def format(self, format_string):
        """Return the date as a string formatted according to 'format_string'."""
        if not format_string or not isinstance(format_string, str):
            message = 'The "format" method takes a string with format codes following the 1989C standard (strftime)'
            raise ValueError(message)

        if '%' not in format_string:  # no date parameters, just a string
            return format_string

        if '%E' in format_string:
            if '%ELy' in format_string:
                format_string = format_string.replace('%ELy', self.get_era(use_ad=True, add_year=True))
            elif '%EL' in format_string:
                format_string = format_string.replace('%EL', self.get_era(use_ad=True))
            elif '%Ey' in format_string:
                format_string = format_string.replace('%Ey', self.get_era(add_year=True))
            format_string = format_string.replace('%E', self.get_era())

        if self.date:
            return self.date.strftime(format_string)

        return self.format_incomplete_date(format_string)

    def format_incomplete_date(self, format_string):
        result = ''
        components = format_string.split('%')
        if not format_string.startswith('%'):
            result = components[0]
            components = components[1:]

        for component in components:
            if component:
                code = component[0]
                rest = component[1:] if len(component) > 1 else None
                # skip if code cannot be handled with an incomplete date or is time-related
                if code not in '+:AGHIMOPRSTUVWXZafgjprsuwz':
                    match code:
                        case 'd' if self.day:
                            result += str(self.day).zfill(2)
                        case 'e' if self.day:
                            result += f' {self.day}'
                        case 'b' if self.month:
                            result += calendar.month_name[self.month]
                        case 'B' if self.month:
                            result += calendar.month_abbr[self.month]
                        case 'm' if self.month:
                            result += str(self.month).zfill(2)
                        case 'C' if self.year:
                            result += math.ceil(self.year / 100)
                        case 'y' if self.year:
                            result += f'{self.year if 1 <= self.year <= 99 else str(self.year)[:-2]}'  # noqa: PLR2004
                        case 'Y' if self.year:
                            result += str(self.year)
                        case 'c':
                            result += self.get_date_string()
                        case 'D':
                            result += self.format('%d/%m/%y')
                        case 'F':
                            result += self.format('%Y-%m-%d')
                        case 'x':
                            result += self.get_date_string()
                        case 'n':
                            result += '\n'
                        case 't':
                            result += '\t'

                    if rest:
                        result += rest
        return result
