import re
from django.template import defaultfilters
from collections import namedtuple


class FormatDalmeDate:
    ''' Class for formatting dates throughout the app '''

    months_long = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    months_short = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    months_int = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    def __init__(self, data):
        if not data:
            raise ValueError('No data supplied')

        self.range = type(data) is list
        self.date = self.get_date(data)

    def get_date(self, data):

        if self.range:
            dateRangeObject = namedtuple('dateRangeObject', 'start, end')
            output = dateRangeObject
            start_d = namedtuple('dateObject', 'day, month, year')
            start_d.day, start_d.month, start_d.year = self.get_date_elements(data[0])
            output.start = start_d
            end_d = namedtuple('dateObject', 'day, month, year')
            end_d.day, end_d.month, end_d.year = self.get_date_elements(data[1])
            output.end = end_d
        else:
            output = namedtuple('dateObject', 'day, month, year')
            output.day, output.month, output.year = self.get_date_elements(data)

        return output

    def get_date_elements(self, date):
        separators = ['-', '/', '.', '—', '–', ' ']
        dt = None
        for s in separators:
            if s in date:
                dt = date.split(s)
                break

        if dt:
            dt = [i for i in dt if i not in ['', ' ', False, None]]
            if len(dt) < 3:
                while len(dt) < 3:
                    dt.insert(0, None)
            return self.get_day(dt), self.get_month(dt), self.get_year(dt)
        else:
            return self.get_day([date]), self.get_month([date]), self.get_year([date])

    @staticmethod
    def get_day(date):
        return date[0] if len(date) == 3 else None

    def get_month(self, date):
        if len(date) > 1:
            if len(date[-2]) == 3:
                m_int = self.months_int[date[-2]]
            else:
                m_int = int(date[-2])
            return m_int
        else:
            return None

    @staticmethod
    def get_year(date):
        return date[-1]

    def format(self, format, detail='full'):
        if detail != 'full':
            detail_method = getattr(self, detail, False)
            if not detail_method:
                raise ValueError('The detail parameter is not valid: it should be "full", "month_year", or "year".')
            date = [detail_method(self.date.start), detail_method(self.date.end)] if self.range else detail_method(self.date)

        else:
            date = [self.date.start, self.date.end] if self.range else self.date

        return self.format_range(date[0], date[1], format) if self.range else self.format_date(date, format)

    @staticmethod
    def month_year(date):
        date.day = None
        return date

    @staticmethod
    def year(date):
        date.day = None
        date.month = None
        return date

    def format_date(self, date, format):
        if date.day is not None:
            if format == 'long':
                return '{} {}, {}'.format(str(date.day), self.months_long[date.month], str(date.year))
            else:
                return '{} {} {}'.format(str(date.day), self.months_short[date.month], str(date.year))

        elif date.month is not None:
            if format == 'long':
                return '{} {}'.format(self.months_long[date.month], str(date.year))
            else:
                return '{} {}'.format(self.months_short[date.month], str(date.year))

        else:
            return str(date.year)

    def format_range(self, start_date, end_date, format):
        if start_date == end_date:
            return self.format_date(start_date, format)
        else:
            if start_date.year == end_date.year:
                if start_date.month == end_date.month and start_date.month is not None:
                    if start_date.day is not None and end_date.day is not None:
                        range_string = '{} to {} {}, {}' if format == 'long' else '{}-{} {} {}'
                        month = self.months_long[start_date.month] if format == 'long' else self.months_short[start_date.month]
                        return range_string.format(str(start_date.day), str(end_date.day), month, str(start_date.year))
                    else:
                        return self.format_date(start_date, format)
                elif start_date.month is not None and end_date.month is not None:
                    start_month = self.months_long[start_date.month] if format == 'long' else self.months_short[start_date.month]
                    end_month = self.months_long[end_date.month] if format == 'long' else self.months_short[end_date.month]
                    if start_date.day is not None and end_date.day is not None:
                        range_string = '{} {} to {} {}, {}' if format == 'long' else '{} {}–{} {} {}'
                        return range_string.format(str(start_date.day), start_month, str(end_date.day), end_month, start_date.year)
                    else:
                        range_string = '{} to {}, {}' if format == 'long' else '{}–{} {}'
                        return range_string.format(start_month, end_month, start_date.year)
            else:
                if start_date.month is not None and end_date.month is not None:
                    start_month = self.months_long[start_date.month] if format == 'long' else self.months_short[start_date.month]
                    end_month = self.months_long[end_date.month] if format == 'long' else self.months_short[end_date.month]
                    if start_date.day is not None and end_date.day is not None:
                        range_string = '{} {}, {} to {} {}, {}' if format == 'long' else '{} {} {} — {} {} {}'
                        return range_string.format(str(start_date.day), start_month, start_date.year, str(end_date.day), end_month, end_date.year)
                    else:
                        range_string = '{} {} to {} {}' if format == 'long' else '{} {} – {} {}'
                        return range_string.format(start_month, start_date.year, end_month, end_date.year)
                else:
                    range_string = '{} to {}' if format == 'long' else '{}–{}'
                    return range_string.format(start_date.year, end_date.year)


def round_timesince(d):
    chunks = {
        'minute': 60,
        'hour': 24,
        'day': 30,
        'week': 4,
        'month': 12
    }
    d_string = defaultfilters.timesince(d)
    if ',' in d_string:
        d_list = re.findall(r"[\w\d']+", d_string)
        for i, j in enumerate(d_list):
            if j[-1] == 's':
                d_list[i] = j[:-1]
        if d_list[3] in ['minute', 'hour']:
            if int(d_list[2]) / chunks[d_list[3]] >= 0.5:
                d_list[0] = int(d_list[0]) + 1
        else:
            if int(d_list[2]) / chunks[d_list[3]] >= 0.2:
                d_list[0] = int(d_list[0]) * chunks[d_list[3]] + int(d_list[2])
                d_list[1] = d_list[3]
        if int(d_list[0]) > 1:
            d_list[1] = d_list[1] + 's'
        result = str(d_list[0]) + ' ' + str(d_list[1]) + ' ago '
    else:
        if d_string == '0\xa0minutes':
            result = 'now'
        else:
            result = d_string + ' ago'
    return result
