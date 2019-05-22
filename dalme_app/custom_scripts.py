"""
Contains general purpose scripts
"""
import re
import os
import json
import pandas as pd
from dalme_app.models import AttributeReference, Language, Attribute
from datetime import date
import calendar


def get_script_menu():
    script_register = [
        {
            "name": "session_info",
            "description": "Outputs the contents of the current session.",
            "type": "info"
        },
        {
            "name": "import_languages",
            "description": "Tests a simple expression that doesn't require complex data or context from the rest of the application.",
            "type": "warning"
        },
        {
            "name": "test_expression",
            "description": "Tests a simple expression that doesn't require complex data or context from the rest of the application.",
            "type": "info"
        },
        {
            "name": "merge_attributes_csv",
            "description": "Parses a .csv file containing attribute values and merges them into the database matching by attribute_id.",
            "type": "danger"
        },
        {
            "name": "add_attribute_types",
            "description": "Takes a dictionary representing a metadata schema and creates entries in the attribute types reference table.",
            "type": "warning"
        }
    ]
    _output = ''
    for item in script_register:
        _output += get_script_menu_item(**item)
    return [_output]


def get_script_menu_item(name=None, description=None, type=None):
    icon_dict = {
        'info': 'fa-info-circle',
        'danger': 'fa-hand-paper',
        'warning': 'fa-exclamation-triangle',
        'secondary': 'fa-scroll',
        'success': 'thumbs-up',
    }
    currentItem = '<a class="script-item d-flex text-dark-gray" href="/scripts?s={}"><div class="script-icon \
                   bg-{}-soft"><i class="fas {} text-{}"></i></div>'.format(name, type, icon_dict[type], type)
    currentItem += '<span class="font-weight-bold mr-1">{}: </span> {}</a>'.format(name, description)
    return currentItem


def add_attribute_types():
    schema = []
    try:
        entries = []
        for i in schema:
            new_entry = AttributeReference()
            new_entry.name = i['Label']
            new_entry.short_name = i['Short Name']
            new_entry.data_type = 'STR'
            new_entry.source = i['URI']
            new_entry.description = i['Definition']
            new_entry.term_type = i['Type of Term']
            if 'Comment' in i:
                new_entry.notes = i['Comment']
            entries.append(new_entry)
        AttributeReference.objects.bulk_create(entries)
        result = 'Cool!'
    except Exception as e:
        result = 'Oops!'+str(e)
    return result


def session_info(request, username):
    output = request.session
    return output


def import_languages(request):
    file = os.path.join('dalme_app', 'templates', 'menus', 'uk.json')
    with open(file, 'r') as fp:
        text = json.load(fp)
        for item in text:
            if not Language.objects.filter(glottolog_id=item['properties']['language']['id']).exists():
                new_lang = Language()
                new_lang.glottolog_id = item['properties']['language']['id']
                new_lang.iso6393_id = item['properties']['language']['hid']
                new_lang.name = item['properties']['language']['name']
                new_lang.type = item['properties']['language']['level']
                new_lang.save()
                if item['properties']['language']['newick']:
                    p = re.compile(r'\'([a-z0-9 ]+) \[(\w+)\]\'', re.IGNORECASE)
                    m = p.findall(item['properties']['language']['newick'])
                    if m:
                        parent_object = Language.objects.get(glottolog_id=item['properties']['language']['id'])
                        for i in m:
                            if not Language.objects.filter(glottolog_id=i[1]).exists():
                                new_dia = Language()
                                new_dia.glottolog_id = i[1]
                                new_dia.name = i[0]
                                new_dia.type = 'dialect'
                                new_dia.parent = parent_object
                                new_dia.save()
    return 'okay'


def test_expression(request):
    val = calendar.month_abbr[3]
    return val


def merge_attributes_csv():
    _file = 'attribute_date.csv'
    _file = os.path.join('dalme_app', _file)
    df = pd.read_csv(_file)
    results = []
    for i, row in df.iterrows():
        att_id = row['attribute_id_id']
        try:
            if not pd.isnull(row['value_day']) and not pd.isnull(row['value_month']):
                day = int(row['value_day'])
                month = int(row['value_month'])
                year = int(row['value_year'])
                the_date = date(year, month, day)
                date_str = the_date.strftime("%d-%b-%Y").lstrip("0").replace(" 0", " ")
                att = Attribute.objects.get(pk=att_id)
                att.value_DATE_d = day
                att.value_DATE_m = month
                att.value_DATE_y = year
                att.value_DATE = the_date
                att.value_STR = date_str
                att.save()
                results.append(str(i) + ', ' + att_id + ': OK')

            elif not pd.isnull(row['value_month']):
                month = int(row['value_month'])
                year = int(row['value_year'])
                the_date = date(year, month, 1)
                date_str = the_date.strftime("%b-%Y")
                att = Attribute.objects.get(pk=att_id)
                att.value_DATE_m = month
                att.value_DATE_y = year
                att.value_STR = date_str
                att.save()
                results.append(str(i) + ', ' + att_id + ': OK')

            else:
                date_str = row['value_year']
                year = int(date_str)
                att = Attribute.objects.get(pk=att_id)
                att.value_DATE_y = year
                att.value_STR = date_str
                att.save()
                results.append(str(i) + ', ' + att_id + ': OK')

        except:
            results.append(str(i) + ', ' + att_id + ': BAD')

    return results
