import re
from django.template import defaultfilters


class DALMEDateRange:
    ''' Class for managing date ranges throughout the app '''

    months_long = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    months_short = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    months_int = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    def __init__(self, start_date, end_date):
        self.long = self.format_range(start_date, end_date, 'long')
        self.short = self.format_range(start_date, end_date, 'short')

    def format_range(self, start_date, end_date, format):
        if start_date == end_date:
            return self.format_date(start_date, format)
        else:
            start_date = self.get_date_elements(start_date, format)
            end_date = self.get_date_elements(end_date, format)
            if start_date[2] == end_date[2]:
                if start_date[1] == end_date[1] and start_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} to {} {}, {}' if format == 'long' else '{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), str(end_date[0]), start_date[1], start_date[2])
                    else:
                        return self.format_date(start_date, format)
                elif start_date[1] is not None and end_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} {} to {} {}, {}' if format == 'long' else '{}/{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), start_date[1], str(end_date[0]), end_date[1], start_date[2])
                    else:
                        range_string = '{} to {}, {}' if format == 'long' else '{}-{}/{}'
                        return range_string.format(start_date[1], end_date[1], start_date[2])
            else:
                if start_date[1] is not None and end_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} {}, {} to {} {}, {}' if format == 'long' else '{}/{}/{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), start_date[1], start_date[2], str(end_date[0]), end_date[1], end_date[2])
                    else:
                        range_string = '{} {} to {} {}' if format == 'long' else '{}/{}-{}/{}'
                        return range_string.format(start_date[1], start_date[2], end_date[1], end_date[2])
                else:
                    range_string = '{} to {}' if format == 'long' else '{}-{}'
                    return range_string.format(start_date[2], end_date[2])

    def get_day(self, date):
        return date[0] if len(date) == 3 else None

    def get_month(self, date, format):
        if len(date) > 1:
            if len(date[-2]) == 3:
                m_int = self.months_int[date[-2]]
            else:
                m_int = int(date[-2])
            return self.months_short[m_int] if format == 'short' else self.months_long[m_int]
        else:
            return None

    def get_year(self, date):
        return date[-1]

    def format_date(self, date, format):
        date = self.get_date_elements(date, format) if type(date) is not list else date
        if date[0] is not None:
            return '{} {}, {}'.format(str(date[0]), date[1], date[2]) if format == 'long' else '{}/{}/{}'.format(str(date[0]), date[1], date[2])
        elif date[1] is not None:
            return '{} {}'.format(date[1], date[2])
        else:
            return date[2]

    def get_date_elements(self, date, format):
        if '-' in str(date):
            date = str(date).split('-')
        else:
            date = [date]
        return [self.get_day(date), self.get_month(date, format), self.get_year(date)]


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
