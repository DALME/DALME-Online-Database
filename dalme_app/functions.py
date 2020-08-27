"""
This file houses all of the miscellaneous functions used elsewhere in the project.
"""
import os
from django.db.models import Q
import json
from random import randint
from dalme_app.models import *
from django.template import defaultfilters
import re
from django.utils import timezone




def get_date_elements(_date):
    if '-' in str(_date):
        return str(_date).split('-')
    else:
        return [_date]
        
def get_date_range(date1, date2):
    output_date = ''
    if date1 == date2:
        output_date = date1
    else:
        date1 = get_date_elements(date1)
        date2 = get_date_elements(date2)

        if len(date1) == len(date2):
            if len(date1) == 3:
                if date1[2] == date2[2]:
                    if date1[1] == date2[1]:
                        output_date = '{} to {}-{}, {}'.format(date1[0], date2[0], date1[1], date1[2])
                    else:
                        output_date = '{}-{} to {}-{}, {}'.format(date1[0], date1[1], date2[0], date2[1], date1[2])
                else:
                    output_date = '{}-{}-{} to {}-{}-{}'.format(date1[0], date1[1], date1[2], date2[0], date2[1], date1[2])
            elif len(date1) == 2:
                if date1[1] == date2[1]:
                    output_date = '{} to {}, {}'.format(date1[0], date2[0], date2[1])
                else:
                    output_date = '{}-{} to {}-{}'.format(date1[0], date1[1], date2[0], date2[1])
            else:
                output_date = '{} to {}'.format(date1[0], date2[0])
        else:
            output_date = '-'.join(date1) + ' to ' + '-'.join(date2)
    return output_date
