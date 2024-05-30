"""Custom class for handling historical dates."""

import calendar
import datetime
import json

from dateutil import parser

MONTH_LONG = calendar.month_name
MONTH_SHORT = calendar.month_abbr
MONTHS_INT = {val: key for key, val in [(i, abbr) for i, abbr in enumerate(MONTH_SHORT) if i != 0]}
SEPARATORS = ['-', '/', '.', '—', '-', ' ']


class HistoricalDate:
    """Class for formatting dates throughout the app.

    Format string should include elements desired from `dmy` and
    length: s (short), l(long). e.g. mys (month-year, short)
    """

    default_keys = ['day', 'month', 'year', 'date', 'text']

    def __init__(self, data):
        if not data:
            message = 'A date in a valid format must be supplied.'
            raise ValueError(message)

        self.day = None  # positive integer in 1-31 range
        self.month = None  # positive integer in 1-12 range
        self.year = None  # integer, length in 1-4 range, negative == BCE
        self.date = None  # Python date object
        self.text = None  # string representation of date
        self.load(data)
        self.is_valid = self.validate_data()

    def __str__(self):
        return self.get_date_string()

    def __eq__(self, other):
        if not isinstance(other, HistoricalDate):
            return NotImplemented
        if self.date and other.date:
            return self.date == other.date
        return self.day == other.day and self.month == other.month and self.year == other.year

    def __lt__(self, other):
        if not isinstance(other, HistoricalDate):
            return NotImplemented
        if self.date and other.date:
            return self.date < other.date
        return self.get_as_months() < other.get_as_months()

    def __le__(self, other):
        if not isinstance(other, HistoricalDate):
            return NotImplemented
        return self.__lt__(other) or self.__eq__(other)

    def __ne__(self, other):
        if not isinstance(other, HistoricalDate):
            return NotImplemented
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, HistoricalDate):
            return NotImplemented
        if self.date and other.date:
            return self.date > other.date
        return self.get_as_months() > other.get_as_months()

    def __ge__(self, other):
        if not isinstance(other, HistoricalDate):
            return NotImplemented
        return self.__gt__(other) or self.__eq__(other)

    def load(self, data):  # noqa: C901, PLR0912
        """Load supplied data."""
        if isinstance(data, str):
            try:
                data = json.loads()
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

        elif isinstance(data, dict):
            self.day = data.get('day')
            self.month = data.get('month')
            self.year = data.get('year')
            self.text = data.get('text')
            date = data.get('date')

            if isinstance(date, (datetime.date | datetime.datetime)):
                self.date = datetime.date(date.year, date.month, date.day)
            elif isinstance(date, str):
                try:
                    date_obj = parser.parse(date)
                    self.date = datetime.date(date_obj.year, date_obj.month, date_obj.day)
                except parser.ParserError:
                    pass

        if self.day and self.month and self.year and not self.date:
            try:
                date = datetime.date(self.year, self.month, self.day)
            except ValueError:
                date = parser.parse(
                    f'{self.year!s}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}',
                )

        if not self.text:
            self.text = self.get_date_string()

    def validate_data(self):
        """Check that the data passed is an actual date."""
        assert any([self.day, self.month, self.year, self.date, self.text]), 'Invalid date: object contains no data.'
        # validate each value
        return True

    def get_date_string(self):
        """Return date string."""
        if self.date is not None:
            return self.date.strftime('%d-%b-%Y').lstrip('0').replace(' 0', ' ')

        if self.month is not None and self.year is not None:
            return f'{calendar.month_abbr[self.month]} {self.year}'

        if self.day is not None and self.month is not None:
            return f'{self.day} {calendar.month_abbr[self.month]}'

        if self.year is not None:
            return str(self.year)

        return 'Unknown date'

    def serialize(self):
        """Return a JSON-serialized version of the date."""
        return {
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'date': self.date.isoformat() if isinstance(self.date, datetime.date) else None,
            'text': self.text,
        }

    def get_as_months(self):
        """Return month/year as a count of months."""
        value = 0
        if self.year:
            value += 12 * self.year
        if self.month:
            value += self.month
        return value
