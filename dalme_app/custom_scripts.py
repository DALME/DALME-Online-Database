"""
Contains general purpose scripts
"""

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.db.models import Q, Count, F, Prefetch
from dalme_app.serializers import *
from rest_framework.response import Response

import re, requests, uuid, os, datetime, json, ast, operator
import pandas as pd

from dalme_app.models import *
from dalme_app import functions
from datetime import date
from django.db.models.expressions import RawSQL
from passlib.apps import phpass_context

def get_script_menu():
    script_register = [
        {
            "name": "session_info",
            "description": "Outputs the contents of the current session.",
            "type": "info"
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
            "name": "import_sources_csv",
            "description": "Used to parse a .csv file containing sources and creating the corresponding records in the database.",
            "type": "danger"
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

def get_script_menu_item(name=None,description=None,type=None):
    icon_dict = {
        'info': 'fa-info-circle',
        'danger': 'fa-hand-paper',
        'warning': 'fa-exclamation-triangle',
        'secondary': 'fa-scroll',
        'success': 'thumbs-up',
    }

    currentItem = '<div class="card-split"><div class="card-split-icon bg-{}-soft"><i class="fas {} text-{}"></i></div><div class="card-split-body">'.format(type, icon_dict[type], type)
    currentItem += '<span class="font-weight-bold text-{} mb-1">{}: </span>'.format(type, name)
    currentItem += '<span class="mb-0 text-dark-gray">{}</span>'.format(description)
    currentItem += '</div><a href="/scripts?s={}" class="btn btn-primary btn-card-split"><span class="icon text-white-50"><i class="fas fa-cogs"></i></span></a></div>'.format(name)

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

def prep_transcriptions ():
    line_types = {
        'house': '8C7A91FB-ACB1-4AC9-B270-3E14E2511C13',
        'room': 'FED9C6D0-3AAC-408B-A285-0EC80B392155',
        'object phrase': '0134DDF8-7816-4C1F-8490-A482F59794B8',
        'context': '2E2712EE-30D0-4A3D-B8D8-4831D35E42B6',
        'container': 'E65E4129-1577-45D9-83A0-6276C8027A5B',
    }
    return x

def session_info(request, username):
    output = request.session
    return output

def test_expression(request):
    data = '{"action":"create","data":{"0":{"user":{"first_name":"John","last_name":"Smith","email":"jsmith@harvard.edu","username":"jsmith","password":"thepassword1234","is_staff":["1"],"is_superuser":["1"],"groups":[{"id":"2"},{"id":"3"},{"id":"4"}],"groups-many-count":3},"full_name":"John Smith","dam_usergroup":{"value":"2"},"wiki_groups":[{"ug_group":"administrator"},{"ug_group":"bureaucrat"}],"wiki_groups-many-count":2,"wp_role":{"value":"a:1:{s:6:\\"author\\";b:1;}"}}}}'
    dt_request = json.loads(data)
    data_dict = dt_request['data']['0']
    return data_dict

def test_expression2():

    dset = {
        'action' : 'create',
        'data[0][user][first_name]' : 'John',
        'data[0][user][last_name]' : 'Smith',
        'data[0][full_name]' : 'John Smith',
        'data[0][user][email]' : 'jsmith@harvard.edu',
        'data[0][user][username]' : 'jsmith',
        'data[0][user][password]' : 'jjsmith1929',
        'data[0][user][is_staff][]' : '1',
        'data[0][user][is_superuser][]' : '1',
        'data[0][user][groups][0][id]' : '3',
        'data[0][user][groups][1][id]' : '4',
        'data[0][groups-many-count]' : '2',
        'data[0][dam_usergroup][value]' : '3',
        'data[0][wiki_groups][0][ug_group]' : 'Bureaucrat',
        'data[0][wiki_groups][1][ug_group]' : 'Sysop',
        'data[0][wiki_groups-many-count]' : '2',
        'data[0][wp_role][value]' : 'a:1:{s:6:"author";b:1;}',
    }

    data = []
    rows = []

    for k,v in dset.items():
        if k != 'action':
            k = json.loads('['+k[4:].replace(']','",').replace('[','"')[:-1]+']')




            for i,f in enumerate(k):
                if 'many-count' in f or f == '' or f.isdigit():
                    k.pop(i)
            if k != []:
                if k[0] == 'user':
                    if len(k) > 1:
                        if k[1] == 'groups':
                            groups.append({k[2]:v})
                        else:
                            user[k[1]] = v
                elif k[0] == 'wiki_groups':
                        wiki_groups.append({k[1]:v})
                else:
                    if len(k) > 1:
                        data_dict[k[0]] = { k[1]:v }
                    else:
                        data_dict[k[0]] = v
        user['groups'] = groups
        data_dict['user'] = user
        data_dict['wiki_groups'] = wiki_groups

    serializer = ProfileSerializer(data=data_dict)
    if serializer.is_valid():
        val = 'yay!'
    else:
        display_fields = ['dam_usergroup', 'wp_role']
        errors = serializer.errors
        fieldErrors = []
        for k,v in errors.items():
            if type(v) is dict:
                for k2, v2 in v.items():
                    field = k+'.'+k2
                    fieldErrors.append({'name':field,'status':str(v2[0])})
            else:
                if k in display_fields:
                    field = k+'.value'
                else:
                    field = k
                fieldErrors.append({'name':field,'status':str(v[0])})
        val = fieldErrors
    return val

def merge_attributes_csv():
    _file = 'attribute_date.csv'
    _file = os.path.join('dalme_app',_file)
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



def import_sources_csv(request, username):
    _file = 'sources_final.csv'
    _file = os.path.join('dalme','dalme_app',_file)
    df = pd.read_csv(_file)

    #first map the columns to the corresponding data-types
    #get column headers
    cols = list(df.columns.values)
    #and adjust for the ones that are imported directly to the sources table, i.e. the first 6 columns
    cols = cols[6:]
    data_types = []
    new_sources = []
    new_attributes = []
    new_attributes_INT = []
    new_attributes_STR = []
    new_attributes_TXT = []
    new_attributes_DBR = []
    new_attributes_DATE = []

    for c in cols:
        if '-2' in c:
            c = c.replace('-2','')

        entry = Attribute_type.objects.get(short_name=c)
        dtype = entry.data_type
        atype = entry.id
        data_types.append((c,atype,dtype))

    #now loop through the rows and create the records
    for i, row in df.iterrows():
        current_row = i

        #first create source record in database
        if not pd.isnull(row['is_inventory']):
            is_inv = True
        else:
            is_inv = False

        #create a new object of "source" type and add the relevant fields
        new_source = Source()
        new_source.id = uuid.UUID(row['id']).hex
        new_source.type = int(row['type'])
        new_source.name = row['name']
        new_source.short_name = row['short_name']

        if not pd.isnull(row['parent_source']):
            new_source.parent_source = uuid.UUID(row['parent_source']).hex

        new_source.is_inventory = is_inv
        new_source.creation_username = username
        new_source.modification_username = username
        #now append it to the list of new sources
        new_sources.append(new_source)

        #source = sources(
        #    id = uuid.UUID(row['id']).hex,
        #    type = int(row['type']),
        #    name = row['name'],
        #    short_name = row['short_name'],
        #    parent_source = uuid.UUID(row['parent_source']).hex,
        #    is_inventory = is_inv,
        #    creation_username=username,
        #    modification_username=username
        #    )
        #source.save()

        #now the attributes
        for a in data_types:
            att = a[0]
            if not pd.isnull(row[att]):
                att_value = row[att]
                atype = a[1]
                dtype = a[2]

                new_attribute = Attribute()
                new_attribute.attribute_type = int(atype)
                new_attribute.content_id = uuid.UUID(row['id']).hex
                new_attribute.creation_username = username
                new_attribute.modification_username = username
                new_attributes.append(new_attribute)

                #attribute = attributes(
                #    attribute_type = int(atype),
                #    content_id = uuid.UUID(row['id']).hex,
                #    creation_username=username,
                #    modification_username=username
                #)
                #attribute.save()
                #att_id = attribute.id

                if dtype == 'INT':
                    new_att_INT = Attribute_INT()
                    new_att_INT.attribute_id = new_attribute
                    new_att_INT.value = int(att_value)
                    new_att_INT.creation_username = username
                    new_att_INT.modification_username = username
                    new_attributes_INT.append(new_att_INT)

                    #att_value = attributes_INT(
                    #    attribute_id = attribute,
                    #    value = int(att_value),
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'STR':
                    new_att_STR = Attribute_STR()
                    new_att_STR.attribute_id = new_attribute
                    new_att_STR.value = att_value
                    new_att_STR.creation_username = username
                    new_att_STR.modification_username = username
                    new_attributes_STR.append(new_att_STR)

                    #att_value = attributes_STR(
                    #    attribute_id = attribute,
                    #    value = att_value,
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'TXT':
                    new_att_TXT = Attribute_TXT()
                    new_att_TXT.attribute_id = new_attribute
                    new_att_TXT.value = att_value
                    new_att_TXT.creation_username = username
                    new_att_TXT.modification_username = username
                    new_attributes_TXT.append(new_att_TXT)

                    #att_value = attributes_TXT(
                    #    attribute_id = attribute,
                    #    value = att_value,
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'DBR':
                    new_att_DBR = Attribute_DBR()
                    new_att_DBR.attribute_id = new_attribute
                    new_att_DBR.value = uuid.UUID(att_value).hex
                    new_att_DBR.creation_username = username
                    new_att_DBR.modification_username = username
                    new_attributes_DBR.append(new_att_DBR)

                    #att_value = attributes_DBR(
                    #    attribute_id = attribute,
                    #    value = uuid.UUID(att_value).hex,
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'DATE':
                    #assemble date elements
                    if '_date_day' in att:
                        d_base = att.replace('_date_day','')
                        d_day = row[att]
                        d_month = row[d_base + '_date_month']
                        d_year = row[d_base + '_date_year']

                        if pd.isnull(d_day) or d_day == '0' or d_day == '?':
                            d_day = ''
                        else:
                            d_day = abs(int(d_day))

                        if pd.isnull(d_month) or d_month == '0' or d_month == '?':
                            d_month = ''
                        else:
                            d_month = abs(int(d_month))

                        if pd.isnull(d_year) or d_year == '0' or d_year == '?':
                            d_year = ''
                        else:
                            d_year = abs(int(d_year))

                        d_date = functions.get_date_from_elements(d_day, d_month, d_year)

                        if d_day or d_month or d_year or d_date:
                            new_att_DATE = Attribute_DATE()
                            new_att_DATE.attribute_id = new_attribute
                            if d_day:
                                new_att_DATE.value_day = d_day
                            if d_month:
                                new_att_DATE.value_month = d_month
                            if d_year:
                                new_att_DATE.value_year = d_year
                            if d_date:
                                new_att_DATE.value = d_date
                            new_att_DATE.creation_username = username
                            new_att_DATE.modification_username = username
                            new_attributes_DATE.append(new_att_DATE)

                        #att_value = attributes_DATE(
                        #    attribute_id = attribute,
                        #    value_day = int(d_day),
                        #    value_month = int(d_month),
                        #    value_year = int(d_year),
                        #    value = d_date,
                        #    creation_username=username,
                        #    modification_username=username
                        #)

    #now run bulk_creates on the relevant models
    Source.objects.bulk_create(new_sources)
    Attribute.objects.bulk_create(new_attributes)
    Attribute_DATE.objects.bulk_create(new_attributes_DATE)
    Attribute_INT.objects.bulk_create(new_attributes_INT)
    Attribute_STR.objects.bulk_create(new_attributes_STR)
    Attribute_TXT.objects.bulk_create(new_attributes_TXT)
    Attribute_DBR.objects.bulk_create(new_attributes_DBR)

    output = 'Everything cool'
    return output
