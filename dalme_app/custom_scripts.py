"""
Contains general purpose scripts
"""
import re
import os
import json
import pandas as pd
from dalme_app.models import AttributeReference, Language, Attribute, Transcription, Source, Attribute_type, DT_fields, Tag, Workset, Task
from datetime import date
from dalme_app.tasks import update_rs_folio_field
from async_messages import messages
from django.contrib.auth.models import User
from dalme_app.apis import normalize_value
from django.db.models.expressions import RawSQL
import operator
from functools import reduce
from django.db.models import Q, Count
from collections import OrderedDict
from django.core.mail import send_mail
from django.http import HttpResponse


def get_script_menu():
    script_register = [
        {
            "name": "session_info",
            "description": "Outputs the contents of the current session.",
            "type": "info"
        },
        {
            "name": "update_folios_in_dam",
            "description": "Updates the contents of the 'folio' field in the DAM to match the value in the corresponding DALME page.",
            "type": "warning"
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
            "name": "test_expression2",
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


def update_folios_in_dam(request):
    user_id = request.user.id
    update_rs_folio_field.delay(user_id)
    return 'Process started...'


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


def test_expression2(request):
    send_mail(
        'Subject, hello G',
        'Here is the message.',
        'DALME Project <mail@dalme.org>',
        ['pizzorno@icloud.com'],
        fail_silently=False,
    )
    return 'done'


def test_expression(request):
    data3 = '{"action":"create","data":{"0":{"title":"some issue","description":"desc","tags":["bug","something"],"url":"https://127.0.0.1.xip.io:8443/models/dt_fields/#","file":"b976cb3c-907e-48b0-b368-ab5e7ab2efd4"}}}'
    dt_request = json.loads(data3)
    dt_request.pop('action')
    rows = dt_request['data']
    data_list = []
    for k, v in rows.items():
        row_values = {}
        for field, value in v.items():
            if 'many-count' not in field:
                if type(value) is list:
                    if len(value) == 1:
                        value = normalize_value(value[0])
                    elif len(value) == 0:
                        value = 0
                    else:
                        value = [normalize_value(i) for i in value]
                elif type(value) is dict:
                    # if len(value) == 1 and value.get('value') is not None:
                    if len(value) == 1:
                        # value = normalize_value(value['value'])
                        value = normalize_value(list(value.values())[0])
                    else:
                        value = {key: normalize_value(val) for key, val in value.items() if 'many-count' not in key}
                else:
                    value = normalize_value(value)
                row_values[field] = value
        data_list.append([k, row_values])
    data_dict = data_list[0][1]
    foo=bar
    fields = data_dict.pop('fields', None)
    if fields is not None:
        if ',' in str(fields):
            fields = fields.split(',')
        else:
            fields = [fields]
    fields = [int(i) for i in fields]
    current_fields = DT_fields.objects.filter(list=1).values_list('field', flat=True)
    add_fields = list(set(fields3) - set(current_fields))
    remove_fields = list(set(current_fields) - set(fields3))
    foo=bar
    attributes = data_dict.pop('attributes', None)
    object = Source.objects.get(pk='4bad6531-67fc-4546-a47b-1a7099fa72f0')
    results = []
    if attributes is not None:
        if 'id' in attributes:
            attributes = [attributes]
        else:
            attributes = list(attributes.values())
        create_attributes = []
        update_attributes = {}
        for a in attributes:
            a_id = a.pop('id')
            a_type = a.pop('attribute_type')
            if a_type is not None:
                a['attribute_type'] = Attribute_type.objects.get(pk=a_type)
                if a_id is not None:
                    update_attributes[a_id] = a
                else:
                    create_attributes.append(a)
        if update_attributes:
            old_attributes = object.attributes.all()
            results.append(old_attributes)
            for att in old_attributes:
                if str(att.id) in update_attributes:
                    up_att = update_attributes.get(str(att.id))
                    att_object = Attribute.objects.get(pk=att.id)
                    # for attr, val in up_att.items():
                    #     setattr(att_object, attr, val)
                    # att_object.save()
                    results.append('to update: '+str(up_att)+str(att_object))
                else:
                    # id = att.id
                    # object.attributes.remove(att)
                    results.append('to delete: '+ str(att))
                    # Attribute.objects.get(pk=id).delete()
        if create_attributes:
            for new_att in create_attributes:
                # object.attributes.create(**new_att)
                results.append('to create: '+str(new_att))
    return results


def import_transcriptions(request):
    data = []
    count = 0
    current_id = 'bc3a2c32639e44d6b5a21829b42ae0b5'
    for e in data:
        # manage counter for folio order
        if e[0] == current_id:
            count = count + 1
        else:
            count = 1
            current_id = e[0]

        # create the transcription record
        new_tr = Transcription()
        new_tr.transcription = e[4]
        new_tr.author = 'smail'
        new_tr.version = 0
        new_tr.save()

        # create the page
        source_object = Source.objects.get(pk=e[0])
        source_object.pages.create(
            name=e[1],
            dam_id=e[2],
            order=count,
            through_defaults={
                    'transcription': new_tr
                }
        )
        # create dan's done tag if necessary
        if e[3] == 1:
            source_object.tags.create(
                tag_type='C',
                tag='Done',
                tag_group='DLS_Lucca_Transcription_Review'
            )

        # update source's has_inventory field
        source_object.has_inventory = 1
        source_object.save()

    return 'done'


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
