"""
Contains general purpose scripts
"""
import re
import os
import json
import pandas as pd
from dalme_app.models import AttributeReference, Language, Attribute, Transcription, Source, Attribute_type, DT_fields, Tag, Workset
from datetime import date
from dalme_app.async_tasks import update_rs_folio_field
from async_messages import messages
from django.contrib.auth.models import User
from dalme_app.apis import normalize_value
from django.db.models.expressions import RawSQL
import operator
from functools import reduce
from django.db.models import Q, Count
from collections import OrderedDict


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
    object = Workset.objects.get(pk=8)
    seq = 3
    qset = json.loads(object.qset)
    qset[str(seq)]['done'] = True
    object.current_record = int(seq) + 1
    object.qset = json.dumps(qset)
    object.save()
    foo=bar
    return 'done'


def test_expression(request):
    data = '{\
        "action": "edit",\
        "data": {\
          "bf137648-c581-4806-932a-5cf741f909dc": {\
            "name": {\
              "name": "Act 2759, Podestà di Lucca 116, 98r-v"\
            },\
            "short_name": "Act 2759, PdL 116",\
            "type": {\
              "id": "13"\
            },\
            "parent": {\
              "id": "78a52237-3bd0-47bf-a071-9c3f76243bdb"\
            },\
            "is_inventory": [\
              "1"\
            ],\
            "pages": {\
              "1": {\
                "order": "1",\
                "name": "98r",\
                "dam_id": "5326"\
              },\
              "2": {\
                "order": "2",\
                "name": "98v",\
                "dam_id": "5327"\
              }\
            },\
            "attributes": {\
              "1": {\
                "type": "28",\
                "value_STR": "Seizure"\
              },\
              "2": {\
                "type": "25",\
                "value_DATE_d": "16",\
                "value_DATE_m": "12",\
                "value_DATE_y": "1342"\
              },\
              "3": {\
                "type": "3",\
                "value_INT": "2759"\
              },\
              "4": {\
                "type": "26",\
                "value_DATE_d": "16",\
                "value_DATE_m": "12",\
                "value_DATE_y": "1342"\
              },\
              "6": {\
                "type": "27",\
                "value_STR": "Lucca.Starter.1"\
              }\
            }\
          }\
        }\
      }'
    data2 = '{"action":"edit","data":{"5d4744eb-5963-43e4-8b81-f45feee2c3ba":{"name":{"name":"Act 6, Podestà di Lucca 33, 3v-4r"},"short_name":"Act 6, PdL 33[test]","type":{"id":"13"},"parent":{"id":"05c64292-62d1-4333-a259-df078155bc8a"},"is_inventory":["1"],"pages":{"1":{"id":"c659c720-4bac-4b0f-9c10-a5a7aa7ab3dc","order":"1","name":"3v","dam_id":"5340"},"2":{"id":"db4dc814-1b68-46d0-af38-cd63a24f1348","order":"2","name":"4r","dam_id":"5341"}},"attributes":{"1":{"id":"49d3da0f-ed7e-45a9-84e1-b47b642b5e50","attribute_type":"3","value_INT":"6"},"2":{"id":"0011eb9f-89e2-49a8-8fd1-746a148b2b57","attribute_type":"28","value_STR":"Seizure"},"3":{"id":"e96389af-c964-458a-b4ad-492676865ebf","attribute_type":"26","value_DATE_d":"9","value_DATE_m":"1","value_DATE_y":"1333"},"7":{"id":"","attribute_type":"35","value_TXT":"new comment TEST"}}}}}'
    data3 = '{"action": "edit","data": {"1": {"name": "Acts & Registers","short_name": "acts_and_registers","description": "List of acts and registers in the database.","api_url": "/api/sources/","helpers": "source_form","fields": "4,17,18,27,2,25,26,42,43,41,38,39,36,28,3","content_types": ""}}}'
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
    fields1 = data_dict.pop('fields', None)
    if fields1 is not None:
        if ',' in str(fields1):
            fields2 = fields1.split(',')
        else:
            fields2 = [fields1]
    fields3 = [int(i) for i in fields2]
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

        # update source's is_inventory field
        source_object.is_inventory = 1
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
