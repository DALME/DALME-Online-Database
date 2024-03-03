"""Define date/time helpers and utilities."""

import calendar
import datetime  # noqa: F401
import re
from collections import namedtuple
from operator import itemgetter

from django.template import defaultfilters

MONTH_LONG = calendar.month_name
MONTH_SHORT = calendar.month_abbr
MONTHS_INT = {val: key for key, val in [(i, abbr) for i, abbr in enumerate(MONTH_SHORT) if i != 0]}
SEPARATORS = ['-', '/', '.', '—', '-', ' ']
TIME_CHUNKS = {
    'minute': 60,
    'hour': 24,
    'day': 30,
    'week': 4,
    'month': 12,
}


class IDADate:
    """Class for formatting dates throughout the app.

    Format string should include elements desired from `dmy` and
    length: s (short), l(long). e.g. mys (month-year, short)
    """

    def __init__(self, data):
        if not data:
            self.raise_error('No date supplied.')

        validated, self.is_range = self.validate_data(data)
        self.text_only = False
        self.start_date = self.get_date_object(validated[0]) if self.is_range else self.get_date_object(validated)
        self.end_date = self.get_date_object(validated[1]) if self.is_range else None
        self.date = self.get_date_range_object(self.start_date, self.end_date) if self.is_range else self.start_date
        self.include = {
            'day': False,
            'month': False,
            'year': False,
        }
        self.format_long = False

    @staticmethod
    def raise_error(message):
        """Raise ValueError exception."""
        raise ValueError(message)

    def validate_data(self, data, is_range=False):
        """Check that the data passed is an actual date or date-range."""
        if isinstance(data, list):
            assert len(data) == 2, 'Invalid date-range: must be a list containing two dates.'  # noqa: PLR2004
            if data[0] == data[1]:
                data = data[0]
            else:
                is_range = True

        data = data if is_range else [data]
        ret = []

        for obj in data:
            obj = eval(obj) if not isinstance(obj, dict) else obj  # noqa: PLW2901
            assert 'day' in obj, 'Invalid date: `day` attribute missing.'
            assert 'month' in obj, 'Invalid date: `month` attribute missing.'
            assert 'year' in obj, 'Invalid date: `year` attribute missing.'
            assert 'date' in obj, 'Invalid date: `date` attribute missing.'
            assert 'text' in obj, 'Invalid date: `text` attribute missing.'
            day, month, year, date, text = itemgetter('day', 'month', 'year', 'date', 'text')(obj)
            assert any([day, month, year, date, text]), 'Invalid date: object contains no data.'
            ret.append(obj)

        return ret if is_range else ret[0], is_range

    @staticmethod
    def get_date_object(data):
        """Return a date object."""
        day, month, year, date, text = itemgetter('day', 'month', 'year', 'date', 'text')(data)
        if all([day is None, month is None, year is None, date is None]):
            Date = namedtuple('dateObject', 'text, text_only')
            return Date(text, text_only=True)
        Date = namedtuple('dateObject', 'day, month, year, text_only')
        return Date(day, month, year, text_only=False)

    def get_date_range_object(self, start, end):
        """Return a date-range object."""
        DateRange = namedtuple('dateRangeObject', 'start, end')
        return DateRange(start, end)

    def format_as(self, format_string):
        """Return date formatted as requested by `format_string`."""
        format_string = format_string.lower().strip()
        assert len(format_string) >= 2, 'Invalid format string, must contain at least two characters.'  # noqa: PLR2004
        assert format_string.endswith(('l', 's')), 'Invalid format string, last character must be `l` or `s`.'
        assert (
            len([i for i in format_string[:-1] if i not in 'dmy']) == 0
        ), 'Invalid format string, unknown character(s) present.'
        self.format_long = format_string[-1] == 'l'
        self.include['day'] = 'd' in format_string
        self.include['month'] = 'm' in format_string
        self.include['year'] = 'y' in format_string

        return self.get_formatted_range() if self.is_range else self.format_date(self.date)

    def format_date(self, date):
        """Return a formatted date string."""
        if date.text_only:
            return date.text
        date_fmt = ''
        if self.include['day'] and date.day:
            date_fmt += f'{date.day} '
        if self.include['month'] and date.month:
            date_fmt += f'{MONTH_LONG[date.month] if self.format_long else MONTH_SHORT[date.month]}, '
        if self.include['year'] and date.year:
            date_fmt += f'{date.year}'
        return date_fmt

    def get_formatted_range(self):
        """Return a formatted date-range string."""
        range_template = '{} to {}' if self.format_long else '{}-{}'
        if self.start_date.text_only or self.end_date.text_only:
            start = self.start_date.text if self.start_date.text_only else self.format_date(self.start_date)
            end = self.end_date.text if self.end_date.text_only else self.format_date(self.end_date)
            return range_template.format(start, end)

        ranges = {
            'day': (
                [self.start_date.day, self.end_date.day]
                if self.include['day'] and self.start_date.day and self.end_date.day
                else []
            ),
            'month': [],
            'year': [],
        }

        for val in ['month', 'year']:
            if self.include[val]:
                if getattr(self.start_date, val):
                    ranges[val].append(getattr(self.start_date, val))
                if getattr(self.end_date, val) and getattr(self.end_date, val) not in ranges[val]:
                    ranges[val].append(getattr(self.end_date, val))

        days = len(ranges['day'])
        months = len(ranges['month'])
        years = len(ranges['year'])

        c1 = ''
        c1 = c1 + f"{ranges['day'][0]} " if days else c1
        c1 = c1 + f"{ranges['month'][0]}" if months > 1 else c1
        c1 = c1 + ', ' if months > 1 and years > 1 else c1
        c1 = c1 + f"{ranges['year'][0]}" if years > 1 else c1

        c2 = ''
        c2 = c2 + f"{ranges['day'][1]} " if days else c2
        c2 = c2 + f"{ranges['month'][-1]}" if months > 0 else c2
        c2 = c2 + ', ' if months > 0 and years > 0 else c2
        c2 = c2 + f"{ranges['year'][-1]}" if years > 0 else c2

        return range_template.format(c1, c2)


def round_timesince(d):
    """Return a rounded time-since string."""
    d_string = defaultfilters.timesince(d)

    if ',' in d_string:
        d_list = re.findall(r"[\w\d']+", d_string)

        for i, j in enumerate(d_list):
            if j[-1] == 's':
                d_list[i] = j[:-1]

        if d_list[3] in ['minute', 'hour']:
            if int(d_list[2]) / TIME_CHUNKS[d_list[3]] >= 0.5:  # noqa: PLR2004
                d_list[0] = int(d_list[0]) + 1

        elif int(d_list[2]) / TIME_CHUNKS[d_list[3]] >= 0.2:  # noqa: PLR2004
            d_list[0] = int(d_list[0]) * TIME_CHUNKS[d_list[3]] + int(d_list[2])
            d_list[1] = d_list[3]

        if int(d_list[0]) > 1:
            d_list[1] = f'{d_list[1]}s'

        return f'{d_list[0]} {d_list[1]} ago'

    return 'now' if d_string == '0\xa0minutes' else f'{d_string} ago'
